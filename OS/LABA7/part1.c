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

    while(1)
    {
        sem_wait(input);

        sleep(1);
        FILE* file = fopen("test.txt","w");
        fprintf(file, "%d", rand() % 9);
        fclose(file);

        sem_post(check);
    }
    sem_close(input);
    sem_close(check);
    sem_unlink(sem_input);
    sem_unlink(sem_check);
    return 0;
}
