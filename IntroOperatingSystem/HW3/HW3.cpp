#include <bits/stdc++.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/time.h>

using namespace std;

const int MAXN = 1000005;
const int NUM_PARTS = 8;

int arr[MAXN];
int n;

// ===== Job Types =====
enum JobType {BUBBLE_SORT, MERGE_SORT};


struct Job{
JobType type;
int start, mid, end; // mid only used in MERGE_SORT
};

// ===== Shared Job Queue =====
queue<Job> job_queue;
pthread_mutex_t queue_mutex = PTHREAD_MUTEX_INITIALIZER;
sem_t job_available;

// ===== Segment Info =====
struct Segment{
    int start, end;
};
Segment segments[15]; // 8 leaf segments + 7 merged
bool segment_done[15];
bool segment_busy[15];
pthread_mutex_t done_mutex = PTHREAD_MUTEX_INITIALIZER;

// ===== Bubble Sort =====
void bubble_sort(int start, int end){
    for (int i = start; i < end - 1; ++i){
        for (int j = start; j < end - 1 - (i - start); ++j){
            if (arr[j] > arr[j + 1]){
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// ===== Merge =====
void merge(int start, int mid, int end){
    vector<int> tmp;
    int i = start, j = mid;
    while (i < mid && j < end){
        if (arr[i] <= arr[j]) 
            tmp.push_back(arr[i++]);
        else 
            tmp.push_back(arr[j++]);
    }
    while (i < mid) tmp.push_back(arr[i++]);
    while (j < end) tmp.push_back(arr[j++]);
    for (int k = 0; k < tmp.size(); ++k){
        arr[start + k] = tmp[k];
    }
}

void check_merge(int left_id, int right_id, int parent_id){
    pthread_mutex_lock(&done_mutex);
    bool ready = segment_done[left_id] && segment_done[right_id];
    bool freeL = !segment_busy[left_id];
    bool freeR = !segment_busy[right_id];
    pthread_mutex_unlock(&done_mutex);


    if (ready && freeL && freeR && !segment_done[parent_id] && !segment_busy[parent_id]){
        int start = segments[left_id].start;
        int mid = segments[right_id].start;
        int end = segments[right_id].end;

        pthread_mutex_lock(&done_mutex);
        segment_busy[parent_id] = true;  // 標記：正在被執行
        pthread_mutex_unlock(&done_mutex);

        pthread_mutex_lock(&queue_mutex);
        job_queue.push({MERGE_SORT, start, mid, end});
        pthread_mutex_unlock(&queue_mutex);
        sem_post(&job_available);
    }
}

// ===== Thread Worker =====
void* worker(void*){
    while (true){
        sem_wait(&job_available);

        pthread_mutex_lock(&queue_mutex);
        if (job_queue.empty()){
            pthread_mutex_unlock(&queue_mutex);
            continue;
        }
        Job job = job_queue.front();
        job_queue.pop();
        pthread_mutex_unlock(&queue_mutex);

        int seg_id = -1;
        for (int i = 0; i < 15; ++i)
            if (segments[i].start == job.start && segments[i].end == job.end){
                seg_id = i;
                break;
            }

        if (seg_id != -1){
            pthread_mutex_lock(&done_mutex);
            segment_busy[seg_id] = true;
            pthread_mutex_unlock(&done_mutex);
        }

        if (job.type == BUBBLE_SORT)
            bubble_sort(job.start, job.end);
        else
            merge(job.start, job.mid, job.end);

        if (seg_id != -1){
            pthread_mutex_lock(&done_mutex);
            segment_done[seg_id] = true;
            segment_busy[seg_id] = false; // 標記執行完畢
            pthread_mutex_unlock(&done_mutex);
        }
    }
    return nullptr;
}

// ===== Input & Output =====
void read_input(const string& filename){
    ifstream fin(filename);
    if (!fin){
        cerr << "[ERROR] Failed to open input file: " << filename << endl;
        exit(1);
    }

    fin >> n;
    for (int i = 0; i < n; ++i){
        fin >> arr[i];
    }
    fin.close();
    return;
}

void write_output(const string& filename){
    ofstream fout;
    fout.open(filename);
    if (!fout) {
        cerr << "[ERROR] Failed to open output file: " << filename << endl;
        exit(1);
    }

    for (int i = 0; i < n; i++){
        fout << arr[i];
        if(i != n - 1) fout << " ";
    }
    fout.close();
}

// ===== Segment Initialization =====
void init_segments(){
    int chunk = n / NUM_PARTS;
    // Level 1 segments (8 segments)
    for (int i = 0; i < NUM_PARTS; ++i)
        segments[i] = {i * chunk, (i == NUM_PARTS - 1) ? n : (i + 1) * chunk};

    // Level 2 merges (8->4)
    segments[8]  = {segments[0].start, segments[1].end};
    segments[9]  = {segments[2].start, segments[3].end};
    segments[10] = {segments[4].start, segments[5].end};
    segments[11] = {segments[6].start, segments[7].end};
    // Level 3 merges (4->2)
    segments[12] = {segments[8].start, segments[9].end};
    segments[13] = {segments[10].start, segments[11].end};
    // Level 4 merge (2->1)
    segments[14] = {segments[12].start, segments[13].end};
}

// ===== Reset All Shared State =====
void reset_all(){
    while (!job_queue.empty()) job_queue.pop();
    memset(segment_done, 0, sizeof(segment_done));
    memset(segment_busy, 0, sizeof(segment_busy));
}

// ===== Core Runner =====
void run_with_threads(int num_threads) {
    reset_all();
    read_input("input.txt");
    
    sem_init(&job_available, 0, 0);
    init_segments();

    pthread_t threads[num_threads];
    for (int i = 0; i < num_threads; ++i)
        pthread_create(&threads[i], NULL, worker, NULL);

    struct timeval start, end;
    gettimeofday(&start, 0);

    // Initial jobs (8 bubble sort)
    for (int i = 0; i < NUM_PARTS; ++i) {
        pthread_mutex_lock(&queue_mutex);
        job_queue.push({BUBBLE_SORT, segments[i].start, 0, segments[i].end});
        pthread_mutex_unlock(&queue_mutex);
        sem_post(&job_available);
    }

    // Monitor and trigger merge jobs
    while (!segment_done[14]) {
        check_merge(0, 1, 8);
        check_merge(2, 3, 9);
        check_merge(4, 5, 10);
        check_merge(6, 7, 11);
        check_merge(8, 9, 12);
        check_merge(10, 11, 13);
        check_merge(12, 13, 14);
        usleep(500);
    }

    gettimeofday(&end, 0);
    double ms = (end.tv_sec - start.tv_sec) * 1000 + (end.tv_usec - start.tv_usec) / 1000.0;
    printf("[Threads=%d] Elapsed time: %.3f ms\n", num_threads, ms);

    string fname = "output_" + to_string(num_threads) + ".txt";
    write_output(fname);
}

// ===== Main =====
int main(){
    for (int t = 7; t <= 8; ++t){
        run_with_threads(t);
    }
    return 0;
}