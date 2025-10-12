#include <iostream>
#include <sys/time.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <sys/wait.h>
#include <cstring>
using namespace std;


typedef unsigned int uint;
uint base[800][800];

void multiply(uint* C, int n, int start, int end){
    for (int i = start; i < end; i++){
        for (int j = 0; j < n; j++){
            uint sum = 0;
            for (int k = 0; k < n; k++)
                sum += base[i][k] * base[k][j];

            C[i * n + j] = sum;
        }
    }
}



int main() {
    cout << "Input the matrix dimension: ";
    int n; 
    cin >> n;
    cout << endl;

    int cnt=0;
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            base[i][j] = cnt;
            cnt++;
        }
    }
    int shmid_C = shmget(IPC_PRIVATE, n*n*sizeof(uint), IPC_CREAT | 0600);
    uint* C = (uint*)shmat(shmid_C, nullptr, 0);

    for(int p=1; p<=16; p++){
        printf("Multiplying matrices using %2d process%s\n", p, ((p == 1)?"":"es"));
        memset(C, 0, n*n*sizeof(uint));
        struct timeval start, end;
        gettimeofday(&start, 0);

        // do something
        for (int child = 0; child < p; ++child){
            pid_t pid = fork();
            if(pid < 0){
                fprintf(stderr, "Fork Failed");
                exit(-1);
            }else if(pid == 0){
                // 子進程：計算一段 row
                int start_row = child * n / p;
                int end_row   = (child + 1) * n / p;
                multiply(C, n, start_row, end_row);
                exit(0);
            }
        }

        for (int i = 0; i < p; ++i)
            wait(nullptr);

        uint sum = 0;
        for (int i = 0; i < n*n; i++)
            sum += C[i];

        // end of doing something
        gettimeofday(&end, 0);
        int sec = end.tv_sec - start.tv_sec;
        int usec = end.tv_usec - start.tv_usec;
        printf("Elapsed time: %f sec, Checksum: %u\n", sec+(usec/1000000.0), sum);
    }


    shmdt(C);
    shmctl(shmid_C, IPC_RMID, nullptr);
    return 0;
}