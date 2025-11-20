#include <bits/stdc++.h>
#include <sys/time.h>

using namespace std;

static const uint64_t PAGE_SIZE = 4096;

struct Access {
    bool is_write;   // true: W, false: R
    uint64_t page;   // page number (offset / 4096)
};

// 讀取 trace 檔，全部載入到 memory buffer（vector<Access>）
bool load_trace(const string &filename, vector<Access> &trace) {
    ifstream fin(filename);
    if (!fin) {
        cerr << "Failed to open trace file: " << filename << endl;
        return false;
    }

    trace.clear();
    trace.reserve(100000000); 
    // 根據投影片說 total references 大約 4,9228,943 筆，先 reserve 一個差不多的空間，避免一直 reallocate

    char op;
    string hex_addr;
    while (fin >> op >> hex_addr) {
        // 轉 16 進位字串成 64-bit 整數
        uint64_t byte_offset = 0;
        try {
            byte_offset = stoull(hex_addr, nullptr, 16);
        } catch (const exception &e) {
            cerr << "Parse error on address: " << hex_addr << " : " << e.what() << endl;
            return false;
        }

        uint64_t page = byte_offset / PAGE_SIZE;

        Access a;
        a.is_write = (op == 'W'); // 其他一律當成 read
        a.page = page;

        trace.push_back(a);
    }

    if (!fin.eof()) {
        // 不是正常 EOF 結束，代表中間有 I/O 問題
        cerr << "Error while reading file (not EOF)." << endl;
        return false;
    }

    return true;
}

struct PageEntry {
    uint64_t page;       // key
    bool dirty;          // true = dirty
    // 是否屬於 clean-first 區域（CFLRU 用）
    bool in_clean_region = false;

    // 是否在 clean page queue 裡（CFLRU 用）
    bool in_clean_queue = false;

    // LRU list 的指標（LRU & CFLRU 共用）
    PageEntry* prev = nullptr;
    PageEntry* next = nullptr;

    // clean page queue 用的link（連 clean-first 區域裡的 clean page）
    PageEntry* cprev = nullptr;
    PageEntry* cnext = nullptr;
};

class LRUList { // 雙向的
public:
    PageEntry *head, *tail;

    LRUList() : head(nullptr), tail(nullptr) {}

    // 把 node 移到 MRU (head)
    void moveToFront(PageEntry* node) {
        if (node == head) return;

        // 先從原位置拔掉
        if (node->prev) node->prev->next = node->next;
        if (node->next) node->next->prev = node->prev;

        if (node == tail)
            tail = node->prev;

        // 插到 head 前面
        node->prev = nullptr;
        node->next = head;
        if (head) head->prev = node;
        head = node;

        if (!tail) tail = head;
    }

    // 插入新節點為 MRU
    void pushFront(PageEntry* node) {
        node->prev = nullptr;
        node->next = head;
        if (head) head->prev = node;
        head = node;

        if (!tail) tail = head;
    }

    // 移除 LRU (tail)
    PageEntry* popBack() {
        if (!tail) return nullptr;
        PageEntry* node = tail;

        if (tail->prev) {
            tail = tail->prev;
            tail->next = nullptr;
        } else {
            head = tail = nullptr;
        }

        return node;
    }
};

class HashTable {
public:
    struct Slot {
        uint64_t key; // page number
        PageEntry* val; // node of LRU list
        bool used;   // slot 是否被用過
        bool deleted;   // slot 是否被刪除過
    };

    vector<Slot> table;
    size_t cap;

    HashTable(size_t frame) {
        cap = frame * 16;
        table.resize(cap);
        for (auto &s : table){
            s.used = false;
            s.deleted = false;
        }
    }

    size_t hash(uint64_t x) const {
        return (x * 50020) % cap;   // 隨便挑一個混合 hash
    }

    PageEntry* get(uint64_t key) {
        size_t h = hash(key);
        for (size_t i = 0; i < cap; i++) {
            size_t idx = (h + i) % cap;
            if (!table[idx].used && !table[idx].deleted) return nullptr; // miss
            if (table[idx].used && table[idx].key == key)
                return table[idx].val;  // hit
        }
        return nullptr;
    }

    void insert(uint64_t key, PageEntry* val) {
        size_t h = hash(key);
        for (size_t i = 0; i < cap; i++) {
            size_t idx = (h + i) % cap;

            if (!table[idx].used) {
                table[idx].used = true;
                table[idx].deleted = false;
                table[idx].key = key;
                table[idx].val = val;
                return;
            }

            if (table[idx].deleted) {
                table[idx].used = true;
                table[idx].deleted = false;
                table[idx].key = key;
                table[idx].val = val;
                return;
            }
        }
    }

    void erase(uint64_t key) {
        size_t h = hash(key);
        for (size_t i = 0; i < cap; i++) {
            size_t idx = (h + i) % cap;
            if (!table[idx].used && !table[idx].deleted) return;
            if (table[idx].used && table[idx].key == key) {
                table[idx].used = false;
                table[idx].deleted = true;
                return;
            }
        }
    }
};

struct LRUCache {
    int capacity;
    int size;
    LRUList list;
    HashTable ht;
    int hits = 0, misses = 0, writebacks = 0;

    LRUCache(int frame) : capacity(frame), size(0), ht(frame) {}

    inline void access(uint64_t page, bool is_write) {
        PageEntry* node = ht.get(page);

        if (node) {
            // HIT
            hits++;
            if (is_write) node->dirty = true;
            list.moveToFront(node);
            return;
        }

        // MISS
        misses++;

        // Cache full → evict LRU
        if (size == capacity) {
            PageEntry* victim = list.popBack();
            if (victim->dirty)
                writebacks++;

            ht.erase(victim->page);
            delete victim;
            size--;
        }

        // Insert new page
        PageEntry* n = new PageEntry{page, is_write, false, false, nullptr, nullptr, nullptr, nullptr};
        list.pushFront(n);
        ht.insert(page, n);
        size++;
    }
};

struct CFLRUCache {
    int capacity;
    int size;
    LRUList list;     // 先跟 LRU 一樣，整條一個 list
    HashTable ht;
    int hits = 0, misses = 0, writebacks = 0;

    // clean-first 區域大小（固定 1/4）
    int clean_region_target;
    int clean_region_size = 0; // 現在有多少頁被標成在 clean-first 區

    // clean-first 區的 "MRU" node
    PageEntry* clean_mru = nullptr;

    // 不是dirty的 page queue 的頭尾
    PageEntry* clean_head = nullptr;  // MRU clean
    PageEntry* clean_tail = nullptr;  // LRU clean

    CFLRUCache(int frame)
        : capacity(frame), size(0), list(), ht(frame) {
        clean_region_target = frame / 4;  // 固定 1/4
    }

    void adjust_region_boundary() {
        // clean region 太大
        while (clean_region_size > clean_region_target) {
            if (!clean_mru) break;

            // clean_mru 要移回 working region → 移出 clean queue
            cleanq_remove(clean_mru);
            clean_mru->in_clean_region = false;
            clean_region_size--;

            clean_mru = clean_mru->cnext; // boundary 往前
        }

        // clean region 太小
        while (clean_region_size < clean_region_target) {
            if (!list.tail) break;  // 沒東西

            PageEntry *cand = nullptr;
            if (!clean_mru) {
                // region 是空的，從 tail 開始
                cand = list.tail;
            } else {
                // region 已經有，往前擴一格
                cand = clean_mru->prev;
            }

            if (!cand) break;   // 已經到 head，沒得擴

            clean_mru = cand;
            add_to_clean_region(clean_mru);
        }
    }

    void cleanq_push_front(PageEntry* n) { // clean queue push front
        n->in_clean_queue = true;
        n->cprev = nullptr;
        n->cnext = clean_head;

        if (clean_head) clean_head->cprev = n;
        clean_head = n;

        if (!clean_tail) clean_tail = n;
    }

    void cleanq_remove(PageEntry* n) {
        if (!n->in_clean_queue) return;

        if (n->cprev) n->cprev->cnext = n->cnext;
        if (n->cnext) n->cnext->cprev = n->cprev;

        if (n == clean_head) clean_head = n->cnext;
        if (n == clean_tail) clean_tail = n->cprev;

        n->cprev = n->cnext = nullptr;
        n->in_clean_queue = false;
    }

    PageEntry* cleanq_pop_back() {
        if (!clean_tail) return nullptr;

        PageEntry* n = clean_tail;
        cleanq_remove(n);
        return n;
    }

    void add_to_clean_region(PageEntry* n) {
        if (!n->in_clean_region) {
            n->in_clean_region = true;
            clean_region_size++;
        }

        // 若 page 是 clean，加入 clean queue
        if (!n->dirty && !n->in_clean_queue) {
            cleanq_push_front(n);
        }
    }

    inline void access(uint64_t page, bool is_write) {
        PageEntry* node = ht.get(page);

        if (node) {
            // HIT
            hits++;
            if (node->dirty == false && is_write) {
                node->dirty = true;
                cleanq_remove(node);   // dirty page 不可以留在 clean queue
            }
            if (node->in_clean_region) {
                node->in_clean_region = false;
                cleanq_remove(node);   // 從 clean queue 移除
                clean_region_size--;

                if (node == clean_mru) {
                    clean_mru = node->next;  // region 變成從下一個開始
                }
            }
            list.moveToFront(node);
            adjust_region_boundary();
            return;
        }

        // MISS
        misses++;

        // 滿了就踢 LRU（暫時先不管 clean-first）
        if (size == capacity) {
            PageEntry* victim = nullptr;

            if (clean_tail) {
                victim = cleanq_pop_back();
                // 也要從 LRU list 移除
                if (victim->prev)
                    victim->prev->next = victim->next;
                else
                    list.head = victim->next;

                if (victim->next)
                    victim->next->prev = victim->prev;
                else
                    list.tail = victim->prev;
                
                victim->prev = victim->next = nullptr;

            }else{
                // 沒 clean → 跟 LRU 一樣：tail 為 victim
                victim = list.popBack();
            }

            if (victim->dirty)
                writebacks++;

            if (victim->in_clean_region) {
                if (victim == clean_mru) {
                    clean_mru = victim->next;
                }
                victim->in_clean_region = false;
                clean_region_size--;     // 必須維護大小
            }

            ht.erase(victim->page);
            delete victim;
            size--;
        }

        // Insert new page
        PageEntry* n = new PageEntry;
        n->page = page;
        n->dirty = is_write;
        n->in_clean_region = false;
        n->in_clean_queue  = false;
        n->prev = n->next = n->cprev = n->cnext = nullptr;

        list.pushFront(n);
        ht.insert(page, n);
        size++;

        adjust_region_boundary();
    }
};

void runLRU(const vector<Access> &trace, int frames) {
    LRUCache cache(frames);

    for (const auto &a : trace){
        cache.access(a.page, a.is_write);
    }
    double ratio = (double)cache.misses / trace.size();

    printf("%d\t%d\t%d\t\t%.10f\t\t%d\n",
           frames, cache.hits, cache.misses, ratio, cache.writebacks);
};

void runCFLRU(const vector<Access> &trace, int frames) {
    CFLRUCache cache(frames);

    for (const auto &a : trace) {
        cache.access(a.page, a.is_write);
    }
    double ratio = (double)cache.misses / trace.size();

    printf("%d\t%d\t%d\t\t%.10f\t\t%d\n",
           frames, cache.hits, cache.misses, ratio, cache.writebacks);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <trace_file_path>" << endl;
        return 1;
    }

    string trace_file = argv[1];
    vector<Access> trace;

    timeval t1, t2;
    gettimeofday(&t1, nullptr);

    bool ok = load_trace(trace_file, trace);
    if (!ok) {
        cerr << "Failed to load trace." << endl;
        return 1;
    }

    gettimeofday(&t2, nullptr);
    double load_time = (t2.tv_sec - t1.tv_sec) + (t2.tv_usec - t1.tv_usec) / 1e6;

    // cout << "Trace loaded. Total accesses = " << trace.size() << endl;
    // cout << "Load time = " << fixed << setprecision(6) << load_time << " sec" << endl;

    cout << "LRU policy:" << endl;
    printf("Frame\tHit\t\tMiss\t\tPage fault ratio\tWrite back count\n");
    gettimeofday(&t1, nullptr);
    
    runLRU(trace, 4096);
    runLRU(trace, 8192);
    runLRU(trace, 16384);
    runLRU(trace, 32768);
    runLRU(trace, 65536);

    gettimeofday(&t2, nullptr);
    double LRU_elapsed_time = (t2.tv_sec - t1.tv_sec) + (t2.tv_usec - t1.tv_usec) / 1e6;
    printf("Total elapsed time: %.6f sec\n\n", LRU_elapsed_time);

    cout << "CFLRU policy:" << endl;
    printf("Frame\tHit\t\tMiss\t\tPage fault ratio\tWrite back count\n");
    gettimeofday(&t1, nullptr);
    
    runCFLRU(trace, 4096);
    runCFLRU(trace, 8192);
    runCFLRU(trace, 16384);
    runCFLRU(trace, 32768);
    runCFLRU(trace, 65536);

    gettimeofday(&t2, nullptr);
    double CFLRU_elapsed_time = (t2.tv_sec - t1.tv_sec) + (t2.tv_usec - t1.tv_usec) / 1e6;
    printf("Total elapsed time: %.6f sec\n\n", CFLRU_elapsed_time);

    return 0;
}