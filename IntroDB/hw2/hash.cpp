#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <cmath>
#include "hash.h"
#include <bitset>
#include "utils.h"

using namespace std;

hash_entry::hash_entry(int key, int value){
    this->key = key;
    this->value = value;
    this->next = nullptr;
}

hash_bucket::hash_bucket(int hash_key, int depth){
    this->local_depth = depth;
    this->num_entries = 0;
    this->hash_key = hash_key;
    this->first = nullptr;
}

/* Free the memory allocated to this->first
*/
void hash_bucket::clear(){
    hash_entry *current = this->first;
    while (current) {
        hash_entry *to_delete = current;
        current = current->next;
        delete to_delete;
    }
    this->first = nullptr;
    this->num_entries = 0;
}

hash_table::hash_table(int table_size, int bucket_size, int num_rows, vector<int> key, vector<int> value){
    this->table_size = table_size; //等於2
    this->bucket_size = bucket_size; //等於3
    this->global_depth = 1;
    bucket_table.resize(table_size, nullptr);

    for (int i = 0; i < table_size; i++) { //初始化hash bucket
        bucket_table[i] = new hash_bucket(i, global_depth);
    }

    for (int i = 0; i < num_rows; i++) {
        insert(key[i], value[i]);
    }
}

/* When insert collide happened, it needs to do rehash and distribute the entries in the bucket.
** Furthermore, if the global depth equals to the local depth, you need to extend the table size.
*/
void hash_table::extend(hash_bucket *bucket){
    if (bucket->local_depth == global_depth) {
        int old_size = table_size;
        table_size *= 2;
        global_depth++;

        bucket_table.resize(table_size, nullptr);
        for (int i = 0; i < old_size; i++) { //把新增加的指到原本
            bucket_table[i + old_size] = bucket_table[i];
        }
    }

    int mask = 1 << bucket->local_depth; //用於區分條目
    bucket->local_depth++;
    hash_bucket *new_bucket = new hash_bucket(bucket->hash_key | mask, bucket->local_depth); //最高位是1的那個bucket

    hash_entry *current = bucket->first;
    hash_entry *old_last = nullptr; //原桶的最後一個entry

    while (current) {
        if (current->key & mask) { //放new_bucket
            if (old_last) { //確認原桶是不是空的
                old_last->next = current->next;
            } else {
                bucket->first = current->next; //把下一個放到原本bucket的第一個
            }
            hash_entry *to_move = current;
            current = current->next; //換下一個entry

            to_move->next = new_bucket->first; //把新的桶子往後推一個
            new_bucket->first = to_move;

            new_bucket->num_entries++; //新桶數量加+1
            bucket->num_entries--; //舊桶數量-1
        } else {
            old_last = current;
            current = current->next; //換下一個entry
        }
    }
    
    //table重新指向
    for(int i=(bucket->hash_key|mask);i<table_size;i+=(1<<(bucket->local_depth))){
         bucket_table[i]=new_bucket;
    }
}

/* When construct hash_table you can call insert() in the for loop for each key-value pair.
*/
void hash_table::insert(int key, int value){

    //找要放哪個bucket
    int hash_index = key & ((1 << global_depth) - 1);
    hash_bucket *bucket = bucket_table[hash_index];
    //找有沒有相同的key
    hash_entry *current = bucket->first;
    while (current) {
        if (current->key == key) {
            current->value = value;
            return;
        }
        current = current->next;
    }

    if (bucket->num_entries < bucket_size) {
        hash_entry *new_entry = new hash_entry(key, value);
        new_entry->next = bucket->first;
        bucket->first = new_entry;
        bucket->num_entries++;
    } else {
        extend(bucket);
        insert(key, value);
    }
}

/* The function might be called when shrink happened.
** Check whether the table necessory need the current size of table, or half the size of table
*/
void hash_table::half_table(){
    if (global_depth <= 1) {
        return;
    }

    for (int i = 0; i < table_size; i++) {
        if (bucket_table[i]->local_depth == global_depth) {
            return;
        }
    }
    global_depth--;
    table_size /= 2;
    bucket_table.resize(table_size);
}

/* If a bucket with no entries, it need to check whether the pair hash index bucket 
** is in the same local depth. If true, then merge the two bucket and reassign all the 
** related hash index. Or, keep the bucket in the same local depth and wait until the bucket 
** with pair hash index comes to the same local depth.
*/
void hash_table::shrink(hash_bucket *bucket){
    // 找到與當前桶對應的另一個桶
    if (bucket->local_depth <= 1) {
        return;
    }

    int pair_bucket_index = bucket->hash_key ^ (1 << (bucket->local_depth - 1));
    hash_bucket *pair_bucket = bucket_table[pair_bucket_index];
    // 如果 pair bucket 和當前 bucket 在相同的 local_depth
    if (pair_bucket->local_depth == bucket->local_depth) {
        // 減少 local_depth
        pair_bucket->local_depth--;

        // 重新映射桶的位置
        bucket_table[bucket->hash_key] = pair_bucket;
        for(int i=bucket->hash_key-(1<<bucket->local_depth) ; i>=0 ; i-=(1<<bucket->local_depth))
            bucket_table[i] = pair_bucket;
        for(int i=bucket->hash_key+(1<<bucket->local_depth) ; i<table_size ; i+=(1<<bucket->local_depth) )
            bucket_table[i] = pair_bucket;

        // 刪除當前 bucket
        delete bucket;

        //檢查shrink完的bucket的pair是不是空著在等
        int pair_pair_bucket_index = pair_bucket->hash_key ^ (1 << (pair_bucket->local_depth - 1));
        hash_bucket *pair_pair_bucket = bucket_table[pair_pair_bucket_index];
        if (pair_pair_bucket->num_entries == 0) {
            shrink(pair_pair_bucket);
        }

        // 檢查是否需要縮減整個哈希表
        half_table();
    }
}

/* When executing remove_query you can call remove() in the for loop for each key.
*/
void hash_table::remove(int key){
    
    //找在哪個bucket
    int hash_index = key & ((1 << global_depth) - 1);
    hash_bucket *bucket = bucket_table[hash_index];

    hash_entry *current = bucket->first;
    hash_entry *prev = nullptr;

    while (current) {
        if (current->key == key) {
            if (prev) { //跳過中間
                prev->next = current->next;
            } else { //如果要找的key在首位
                bucket->first = current->next;
            }
            delete current;
            bucket->num_entries--;
            break;
        }
        prev = current;
        current = current->next;
    }

    if (bucket->num_entries == 0) {
        shrink(bucket);
    }

}

void hash_table::key_query(vector<int> query_keys, string file_name) {
    ofstream file(file_name);
    file << global_depth << endl;
    for (int key : query_keys) {
        int hash_index = key & ((1 << global_depth) - 1);
        hash_bucket* bucket = bucket_table[hash_index];
        hash_entry* current = bucket->first;

        int value = -1;
        while (current) {
            if (current->key == key) {
                value = current->value;
                break;
            }
            current = current->next;
        }
        file << value << "," << bucket->local_depth << endl;
    }
    file.close();
}

void hash_table::remove_query(vector<int> query_keys){
    for (int key : query_keys) {
        remove(key);
    }
}

/* Free the memory that you have allocated in this program
*/
void hash_table::clear(){
    for (hash_bucket *bucket : bucket_table) {
        if (bucket) {
            bucket->clear();
        }
    }
}
