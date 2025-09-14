#include <bits/stdc++.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
using namespace std;

vector<char*> parse_args(vector<char*> args, int start, int end){
    vector<char*> new_args;
    for(int i = start; i < end; i++){
    new_args.push_back(args[i]);
    }
    new_args.push_back(nullptr);
    return new_args;
}

int main(){
    signal(SIGCHLD, SIG_IGN);
    while(1){
        string cmd;
        cout << ">";
        getline(cin, cmd);
        vector<char*> args;
        bool is_background = false;
        int pipe_idx = -1;

        // 移除結尾換行
        if(!cmd.empty() && cmd.back() == '\n')
            cmd.pop_back();
        
        // 將字串分割
        stringstream ss(cmd);
        string token;
        string infile = "", outfile = "";
        while(ss >> token){
            if(token == "&"){
                is_background = true;
            }else if(token == ">"){
                ss >> outfile;
            }else if(token == "<"){
                ss >> infile;
            }else if(token == "|"){
                pipe_idx = args.size();
            }else{
                // strdup 回傳的是 new 出來的 char*
                args.push_back(strdup(token.c_str()));
            }
        }
        args.push_back(nullptr); // execvp 需要以 nullptr 結尾
        // pipe 處理
        if(pipe_idx != -1){
            vector<char*> left_args = parse_args(args, 0, pipe_idx);
            vector<char*> right_args = parse_args(args, pipe_idx, args.size()-1);

            int pipefd[2];
            pipe(pipefd); //pipefd[0] for read, pipefd[1] for write
            pid_t pid1 = fork();
            if(pid1 < 0){
                fprintf(stderr, "Fork Failed");
                exit(-1);
            }else if(pid1 == 0){
                close(pipefd[0]);
                dup2(pipefd[1], STDOUT_FILENO);
                close(pipefd[1]);
                if (execvp(left_args[0], left_args.data()) == -1){
                    perror("execvp failed");
                    exit(1);
                }
            }

            pid_t pid2 = fork();
            if(pid2 < 0){
                fprintf(stderr, "Fork Failed");
                exit(-1);
            }else if(pid2 == 0){
                close(pipefd[1]);
                dup2(pipefd[0], STDIN_FILENO);
                close(pipefd[0]);
                if (execvp(right_args[0], right_args.data()) == -1){
                    perror("execvp failed");
                    exit(1);
                }
            }

            close(pipefd[0]);
            close(pipefd[1]);
            waitpid(pid1, NULL, 0);
            waitpid(pid2, NULL, 0);
            for(auto ptr : args) free(ptr);
        }else{
            pid_t pid = fork();
            if(pid < 0){
                fprintf(stderr, "Fork Failed");
                exit(-1);
            }else if(pid == 0){
                // child process
                // IO redirection
                if (!outfile.empty()) {
                    int fd = open(outfile.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644); //0644 = rw-r--r--
                    if (fd < 0) { perror("open > failed"); exit(1); }
                    dup2(fd, STDOUT_FILENO);
                    close(fd);
                }

                if (!infile.empty()) {
                    int fd = open(infile.c_str(), O_RDONLY);
                    if (fd < 0) { perror("open < failed"); exit(1); }
                    dup2(fd, STDIN_FILENO);
                    close(fd);
                }

                // execution
                if (execvp(args[0], args.data()) == -1){
                    perror("execvp failed");
                    exit(1);
                }
            }else{
                // parent process
                if(!is_background){
                    waitpid(pid, nullptr, 0); // wait for child process
                }else{
                    cout << "[Background PID " << pid << "]" << endl;
                }
            }

            for(auto ptr : args) free(ptr);
        }  
    }
        
    return 0;
}