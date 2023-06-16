#include <semaphore.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main()
{
    sem_t *input;
    sem_t *check;
    const char *sem_input = "input";
    const char *sem_check = "check";
    input = sem_open(sem_input, O_CREAT, 0777, 1);
    check = sem_open(sem_check, O_CREAT, 0777, 0);

    char buf[2];

    while(1)
    {
        sem_wait(check);

        FILE* file=fopen("test.txt","r");
        fgets(buf, 2, file);
        fclose(file);
        int n = atoi(buf);
        for (int i = 0; i < n; i++)
        {
            printf("%s", "a");
        }
        printf("\n");

        sem_post(input);
    }
    sem_close(input);
    sem_close(check);
    sem_unlink(sem_input);
    sem_unlink(sem_check);
    return 0;
}
