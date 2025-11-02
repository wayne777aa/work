#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>

#define LEVELS 11
#define HEADER_SIZE 32


typedef struct BlockHeader{
    size_t size;
    int free;
    struct BlockHeader *next; // for free list in same level
}BlockHeader;

static void* pool_start = NULL;         // mmap base address
static BlockHeader* free_lists[LEVELS]; // multilevel free lists
static int initialized = 0;             // first-time flag

// Find the free list level index for a given size
int find_level(size_t size){
    size_t lower = 32;
    if(size < lower) return 0;

    for(int i = 1; i < LEVELS; i++){
        size_t upper = lower * 2;
        if (size < upper) return i;
        lower = upper;
    }
    return LEVELS - 1;
}

// Align size to the next multiple of 32
size_t align_size(size_t size){
    if(size % 32 != 0)
        size += (32 - (size % 32));
    return size;
}

void add_to_free_list(BlockHeader *blk){
    blk->free = 1;
    blk->next = NULL;

    int lvl = find_level(blk->size);
    if(!free_lists[lvl]){
        free_lists[lvl] = blk;
    }else{
        BlockHeader *cur = free_lists[lvl];
        while (cur->next)
            cur = cur->next;
        cur->next = blk;
    }
}

void remove_from_free_list(BlockHeader *blk){
    int lvl = find_level(blk->size);
    BlockHeader *cur = free_lists[lvl];
    BlockHeader *prev = NULL;

    while(cur){
        if(cur == blk){
            if (prev)
                prev->next = cur->next;
            else
                free_lists[lvl] = cur->next;
            break;
        }
        prev = cur;
        cur = cur->next;
    }
    blk->next = NULL;
}

BlockHeader *split_block(BlockHeader *blk, size_t req_size){
    size_t total = blk->size + HEADER_SIZE; // total size including header
    if(total >= req_size + HEADER_SIZE){ // can split into two blocks
        BlockHeader *new_blk = (BlockHeader *)((char *)blk + req_size);
        new_blk->size = total - req_size - HEADER_SIZE;
        new_blk->free = 1;
        new_blk->next = NULL;
        add_to_free_list(new_blk);
        blk->size = req_size - HEADER_SIZE;
    }
    return blk;
}

BlockHeader* find_prev_block(BlockHeader* blk){
    BlockHeader* cur = (BlockHeader*)pool_start;
    BlockHeader* prev = NULL;

    while(cur && (char*)cur < (char*)blk){
        prev = cur;
        cur = (BlockHeader*)((char*)cur + HEADER_SIZE + cur->size);
    }

    return (prev == blk) ? NULL : prev;
}

BlockHeader* merge(BlockHeader* blk){
    // merge next
    BlockHeader* next_blk = (BlockHeader*)((char*)blk + blk->size + HEADER_SIZE);
    if((char*)next_blk < (char*)pool_start + 20000 && next_blk->free){
        remove_from_free_list(next_blk);
        blk->size += next_blk->size + HEADER_SIZE;
    }

    // merge prev
    BlockHeader* prev_blk = find_prev_block(blk);
    if(prev_blk && prev_blk->free){
        remove_from_free_list(prev_blk);
        prev_blk->size += blk->size + HEADER_SIZE;
        blk = prev_blk;
    }

    return blk;
}

BlockHeader* find_best_fit(size_t size){
    int level = find_level(size);
    BlockHeader* best_fit = NULL;

    for(int i = level; i < LEVELS; i++){
        BlockHeader* cur = free_lists[i];
        while(cur){
            if(cur->free && cur->size >= size){
                if(!best_fit || cur->size < best_fit->size){
                    best_fit = cur;
                }
            }
            cur = cur->next;
        }
        if (best_fit) break;
    }

    if(best_fit)
        remove_from_free_list(best_fit);
    
    return best_fit;
}

void *malloc(size_t size){
    // initial free block
    if(!initialized){
        pool_start = mmap(NULL, 20000, PROT_READ | PROT_WRITE, MAP_ANON | MAP_PRIVATE, -1, 0);
        if(pool_start == MAP_FAILED){
            _exit(1);
        }
        BlockHeader* blk = (BlockHeader*)pool_start;
        blk->size = 20000 - HEADER_SIZE;
        blk->free = 1;
        blk->next = NULL;

        int lvl = find_level(blk->size);
        free_lists[lvl] = blk;

        initialized = 1;
    }
    // special case: end-of-test signal
    if(size == 0){

        size_t max_free = 0;
        for(int i = 0; i < LEVELS; i++){
            BlockHeader* cur = free_lists[i];
            while(cur){
                if (cur->free && cur->size > max_free)
                    max_free = cur->size;
                cur = cur->next;
            }
        }

        char buf[128];
        int len = sprintf(buf, "Max Free Chunk Size = %zu\n", max_free);
        write(STDOUT_FILENO, buf, len);

        munmap(pool_start, 20000);
        initialized = 0;
        return NULL;
    }

    size = align_size(size);
    size_t total_size = size + HEADER_SIZE;
    BlockHeader* blk = find_best_fit(size);
    if(!blk) return NULL; // no space

    blk = split_block(blk, total_size);
    blk->free = 0;
    return (char*)blk + HEADER_SIZE;
}

void free(void *ptr){
    if(!ptr || !initialized)
        return;

    BlockHeader *blk = (BlockHeader *)((char *)ptr - HEADER_SIZE);
    blk->free = 1;
    blk = merge(blk);
    add_to_free_list(blk);
}