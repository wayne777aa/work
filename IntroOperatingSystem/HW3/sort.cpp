#include <bits/stdc++.h>
using namespace std;


const int MAXN = 1000005;
int arr[MAXN];
int n;


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

int main() {
    read_input("input.txt");
    
    sort(arr, arr + n);

    // 寫入 output_1.txt
    write_output("output_sample.txt");

    return 0;
}