#define FUSE_USE_VERSION 30
#include <fuse.h>
#include <string.h>
#include <bits/stdc++.h>
using namespace std;

struct TarHeader {
    char name[100];      // 0
    char mode[8];        // 100
    char uid[8];         // 108
    char gid[8];         // 116
    char size[12];       // 124
    char mtime[12];      // 136
    char chksum[8];      // 148
    char typeflag;       // 156
    char linkname[100];  // 157
    char magic[8];       // 257
    char uname[32];      // 265
    char gname[32];      // 297
    char devmajor[8];    // 329
    char devminor[8];    // 337
    char prefix[167];    // 345 (padding / other fields)
};


/// octal → decimal (TAR 格式用八進位 ASCII)
size_t oct2dec(const char *str, size_t size) {
    size_t num = 0;
    for (size_t i = 0; i < size && str[i]; i++) {
        if (str[i] >= '0' && str[i] <= '7')
            num = (num << 3) + (str[i] - '0'); // num = num*8 + digit
    }
    return num;
}

struct TarEntry {
    string name;
    mode_t mode;
    uid_t uid;
    gid_t gid;
    size_t size;
    time_t mtime;
    char typeflag;
    string linkname;
    vector<char> data;
};

unordered_map<string, TarEntry> fs;
unordered_map<string, vector<string>> children;


void load_tar(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        perror("Cannot open tar file");
        exit(1);
    }

    while (true) {
        TarHeader header;
        size_t n = fread(&header, 1, 512, fp);
        if (n < 512) break;

        // Check if this is the end-of-archive block (all zero)
        bool empty = true;
        for (int i = 0; i < 512; i++) {
            if (((unsigned char*)&header)[i] != 0) {
                empty = false;
                break;
            }
        }
        if (empty) break;

        // --------------------------
        // Parse fields
        // --------------------------

        // name
        string filename_str(header.name, strnlen(header.name, 100));

        // 都是八進位 ASCII
        mode_t mode = oct2dec(header.mode, 8);
        size_t filesize = oct2dec(header.size, 12);
        time_t mtime = oct2dec(header.mtime, 12);
        uid_t  uid = oct2dec(header.uid, 8);
        gid_t  gid = oct2dec(header.gid, 8);

        char typeflag = header.typeflag;

        // symbolic link target
        string linkname_str(header.linkname, strnlen(header.linkname, 100));

        // --------------------------
        // Build TarEntry
        // --------------------------
        TarEntry entry;

        string name = filename_str;
        if (!name.empty() && name.back() == '/')
            name.pop_back();

        entry.name = name;

        entry.mode = mode;
        entry.size = filesize;
        entry.mtime = mtime;
        entry.uid = uid;
        entry.gid = gid;
        entry.typeflag = typeflag;
        entry.linkname = linkname_str;

        // --------------------------
        // Load file content (only for file type)
        // --------------------------
        if (typeflag == '\0' || typeflag == '0') {  // regular file
            entry.data.resize(filesize);
            fread(entry.data.data(), 1, filesize, fp);
        } else {
            // directory or symlink: no data block
            fseek(fp, filesize, SEEK_CUR);
        }

        // --------------------------
        // Skip padding (round up to 512 bytes)
        // --------------------------
        size_t padding = (512 - (filesize % 512)) % 512;
        fseek(fp, padding, SEEK_CUR);

        // store entry
        fs[entry.name] = entry;

        
        // --------------------------
        // 建立 children map
        // --------------------------
        string full = entry.name;

        // 去掉末尾 '/'
        if (!full.empty() && full.back() == '/')
            full.pop_back();

        string parent;
        size_t pos = full.rfind('/');

        if (pos == string::npos) {
            // 放在 root/
            parent = "";
            children[""].push_back(full);
        } else {
            parent = full.substr(0, pos);
            string child = full.substr(pos + 1);
            children[parent].push_back(child);
        }
    }

    fclose(fp);
}

int my_readdir(const char *path, void *buffer, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi) {
    string dir = path;

    // 檢查這個 path 是否存在且是一個目錄
    if (dir != "/") {
        string key = path;
        if (key[0] == '/') key = key.substr(1);

        auto entry_it = fs.find(key);
        
        if (entry_it == fs.end()) {
            return -ENOENT; // 檔案/目錄不存在
        }
        
        // 確保它是目錄 (typeflag '5' 或 root dir)
        if (entry_it->second.typeflag != '5') {
            return -ENOTDIR; // 不是目錄
        }
    }

    // 先填 . 和 ..
    filler(buffer, ".", NULL, 0);
    filler(buffer, "..", NULL, 0);

    // 處理 path 轉成 children key
    

    // root "/" 對應 key=""
    if (dir == "/") {
        dir = "";
    } else if (dir[0] == '/') {
        dir = dir.substr(1); // 去掉 '/'
    }

    // 看看這個 key 是否存在 children
    auto it = children.find(dir);
    if (it == children.end()) {
        return 0; // 空目錄
    }

    // 填入每個 child name
    for (auto &name : it->second) {
        filler(buffer, name.c_str(), NULL, 0);
    }

    return 0;
}

int my_getattr(const char *path, struct stat *st) {
    memset(st, 0, sizeof(struct stat));

    // ------------------------------------
    // 1. 處理 root "/" 特例
    // ------------------------------------
    if (strcmp(path, "/") == 0) {
        st->st_mode = S_IFDIR | 0444;  // read-only directory
        return 0;
    }

    // 去掉前面的 '/'
    string key = path;
    if (key[0] == '/') key = key.substr(1);

    // ------------------------------------
    // 2. 在 fs map 找 entry
    // ------------------------------------
    auto it = fs.find(key);
    if (it == fs.end()) {
        return -ENOENT;
    }

    TarEntry &e = it->second;

    st->st_uid = e.uid;
    st->st_gid = e.gid;
    st->st_mtime = e.mtime;
    st->st_size = e.size;

    // ------------------------------------
    // 3. 設定 st_mode（根據 typeflag）
    // ------------------------------------
    mode_t access_mode = e.mode & 0777; // 只保留 9 個權限位元 (rwxrwxrwx)

    if (e.typeflag == '5') {
        // directory
        st->st_mode = S_IFDIR | access_mode;
    }
    else if (e.typeflag == '2') {
        // symbolic link
        st->st_mode = S_IFLNK | access_mode;
    }
    else {
        // regular file ('0' or '\0')
        st->st_mode = S_IFREG | access_mode;
    }

    return 0;
}

int my_read(const char *path, char *buffer, size_t size, off_t offset, struct fuse_file_info *fi) {
    // 去掉 '/'
    string key = path;
    if (key.size() > 1 && key[0] == '/')
        key = key.substr(1);

    // 找檔案
    auto it = fs.find(key);
    if (it == fs.end())
        return -ENOENT;

    TarEntry &e = it->second;

    // 只能讀 regular file
    if (!(e.typeflag == '0' || e.typeflag == '\0'))
        return -EISDIR;  // 如果不是檔案，報錯

    size_t fsize = e.size;

    // offset 超過檔案大小 → EOF
    if (offset >= fsize)
        return 0;

    // 計算剩餘可讀大小
    size_t bytes_to_read = min(size, fsize - (size_t)offset);

    // 複製資料到 buffer
    memcpy(buffer, e.data.data() + offset, bytes_to_read);

    return bytes_to_read;
}

int my_readlink(const char *path, char *buffer, size_t size) {
    // 去掉 '/'
    string key = path;
    if (key.size() > 1 && key[0] == '/')
        key = key.substr(1);

    // 找到 entry
    auto it = fs.find(key);
    if (it == fs.end())
        return -ENOENT;

    TarEntry &e = it->second;

    // 必須是 symbolic link
    if (e.typeflag != '2')
        return -EINVAL;  // invalid argument

    // 複製 link target 到 buffer
    size_t len = e.linkname.size();
    if (len >= size) len = size - 1;  

    memcpy(buffer, e.linkname.c_str(), len);
    buffer[len] = '\0';  // 保險起見，加上結尾 NULL

    return 0;
}

static struct fuse_operations op;

int main(int argc, char *argv[]){
    load_tar("test.tar");
    
    memset(&op, 0, sizeof(op));
    op.getattr = my_getattr;
    op.readdir = my_readdir;
    op.read = my_read;
    op.readlink = my_readlink;
    return fuse_main(argc, argv, &op, NULL);
}