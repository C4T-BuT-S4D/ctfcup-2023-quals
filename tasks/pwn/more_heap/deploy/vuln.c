#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <fcntl.h>

#define MAX_NOTES 10

void menu() {
    write(1, "1. Add\n2. Delete\n3. Edit\n4. Show\n5. Exit\n\n> ", 44);
}

void init() {
    struct sock_filter filter[] = {
        {0x20, 0, 0, 0x00000004},
        {0x15, 0, 12, 0xc000003e},
        {0x20, 0, 0, 0x00000000},
        {0x15, 9, 0, 0x00000000},
        {0x15, 8, 0, 0x00000001},
        {0x15, 7, 0, 0x00000101},
        {0x15, 6, 0, 0x0000003c},
        {0x15, 5, 0, 0x000000e7},
        {0x15, 4, 0, 0x0000013e},
        {0x15, 3, 0, 0x000000e4},
        {0x15, 2, 0, 0x000000ca},
        {0x15, 1, 0, 0x0000000c},
        {0x5, 0, 0, 0x00000001},
        {0x6, 0, 0, 0x7fff0000},
        {0x6, 0, 0, 0x00000000},
    };

    struct sock_fprog prog = {
        .len = (sizeof(filter)) / sizeof(struct sock_filter),
        filter,
    };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

char *notes[MAX_NOTES];

char check(unsigned long addr) {
    unsigned long stack, bin;
    stack = &stack;
    stack &= 0xffffffffffff0000;
    if ((addr & 0xfffffffffff0000) == stack) return 0;

    // unsigned long libc = &read;
    // libc -= 0x114980;
    // if ((libc <= addr) && (addr <= libc + 0x21b000)) return 0;

    bin = &init;
    bin &= 0xffffffffffff0000;
    if ((addr & 0xfffffffffff0000) == bin) return 0;

    return 1;
}

void add() {
    unsigned int idx;
    write(1, "Index: ", 7);
    read(0, &idx, sizeof(idx));
    if (!(idx < MAX_NOTES)) {
        write(1, "BAN\n", 4);
        return;
    }
    char buf[0x10];
    *(long*)(buf) = 0;
    *(long*)(buf+8) = 0;
    write(1, "Note: ", 6);
    read(0, buf, sizeof(buf));
    for (int i = 0; i < 0x10; ++i) {
        if (*(unsigned int*)(buf+i) == 0x67616c66) {
            write(1, "BAN\n", 4);
            return;
        }
    }
    notes[idx] = malloc(sizeof(buf));
    if (!check(notes[idx])) {
        free(notes[idx]);
        notes[idx] = 0;
        write(1, "BAN\n", 4);
        return;
    }
    *(long*)(notes[idx]) = *(long*)(buf);
    *(long*)(notes[idx]+8) = *(long*)(buf+8);
}

void delete() {
    unsigned int idx;
    write(1, "Index: ", 7);
    read(0, &idx, sizeof(idx));
    if (!(idx < MAX_NOTES)) {
        write(1, "BAN\n", 4);
        return;
    }
    free(notes[idx]);
}

void show() {
    unsigned int idx;
    write(1, "Index: ", 7);
    read(0, &idx, sizeof(idx));
    if (!(idx < MAX_NOTES)) {
        write(1, "BAN\n", 4);
        return;
    }
    char *s = notes[idx];
    while (*s != '\0') {
        write(1, s++, 1);
    }
    write(1, "\n", 1);
}

void edit() {
    write(1, "What?\n", 6);
}


int main() {
    init();
    char s[4] = {};
    while (1) {
        menu();
        read(0, &s, 2);
        if (s[1] != '\0' && s[1] != '\n') {
            write(1, "Invalid choice\n", 15);
            continue;
        }
        if (s[0] == '1') {
            add();
        }
        else if (s[0] == '2') {
            delete();
        }
        else if (s[0] == '3') {
            edit();
        }
        else if (s[0] == '4') {
            show();
        }
        else if (s[0] == '5') {
            // __asm__(
            //     ".intel_syntax noprefix;"
            //     "xor edi, edi;"
            //     "mov eax, 0x3c;"
            //     "syscall;"
            //     ".att_syntax;"
            // );
            _exit(0);
        }
        else {
            write(1, "Invalid choice\n", 15);
            continue;
        }
    }
    return 0;
}