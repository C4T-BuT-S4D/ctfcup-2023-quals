#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <seccomp.h>
#include <syscall.h>

char ella_buf[0x100];

void __attribute__((constructor)) seccomp()
{
    alarm(5);

    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_read, 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_write, 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_exit_group, 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_newfstatat, 1, SCMP_A0(SCMP_CMP_EQ, 0));
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_lseek, 1, SCMP_A0(SCMP_CMP_EQ, 0));
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, __NR_openat, 1, SCMP_A2(SCMP_CMP_EQ, 0));
    seccomp_load(ctx);
}

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    strcpy(ella_buf, "New laws oppressing elves and giants were issued!");
}

void menu() {
    printf("Hi! I'm Ella Enchanted and you can ask me anything!\nType 1 to send a letter\nType 2 to open a Christmas present box\nType 3 to read a newspaper\nChoice: ");
}

int read_option() {
    int x = 0;
    scanf("%d", &x);
    return x;
}

void ella_write() {
    printf("Enter text of the letter: ");
    unsigned long long text = 0;
    scanf("%llx", &text);
    printf("Enter destination of the letter: ");
    unsigned long long destination = 0;
    scanf("%llx", &destination);
    *(unsigned long long *)(destination) = text;
    puts("I've sent your letter!");
}

void ella_open() {
    int fd = open("/flag.txt", O_RDONLY);
    read(fd, ella_buf, 0x100);
    *strchrnul(ella_buf, '\n') = '\0';
    puts("I've opened a Christmas present box!");
}

void ella_print() {
    puts(ella_buf);
}

void incorrect_option() {
    puts("I can't do that");
}

int main() {
    setup();
    menu();
    int option = read_option();

    if (option == 1) {
        ella_write();
    } else if (option == 2) {
        ella_open();
    } else if (option == 3) {
        ella_print();
    } else {
        incorrect_option();
    }
}
