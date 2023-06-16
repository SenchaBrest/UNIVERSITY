#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
    pid_t pid;
    printf("Порождение процесса 1 PID=%d PPID=%d\n", getpid(), getppid());

    if ((pid = fork()) < 0)
    {
        printf("Ошибка при порождении процесса 2!\n");
        exit(1);
    }
    else if (pid == 0)
    {
        printf("Порождение процесса 2 (от процесса 1) PID=%d PPID=%d\n", getpid(), getppid());

        if ((pid = fork()) < 0)
        {
            printf("Ошибка при порождении процесса 4!\n");
            exit(1);
        }
        else if (pid == 0)
        {
            printf("Порождение процесса 4 (от процесса 2) PID=%d PPID=%d\n", getpid(), getppid());
            printf("Завершился процесс 4 PID=%d PPID=%d\n", getpid(), getppid());
            exit(0);
        }
        else sleep(1);

        if ((pid = fork()) < 0)
        {
            printf("Ошибка при порождении процесса 5!\n");
            exit(1);
        }
        else if (pid == 0)
        {
            printf("Порождение процесса 5 (от процесса 2) PID=%d PPID=%d\n", getpid(), getppid());
            printf("Завершился процесс 5 PID=%d PPID=%d\n", getpid(), getppid());
            execl("/bin/df","df",NULL);
            exit(0);
        }
        else sleep(1);

        printf("Завершился процесс 2 PID=%d PPID=%d\n", getpid(), getppid());
        exit(0);
    }
    else sleep(1);
    


    if ((pid = fork()) < 0)
    {
        printf("Ошибка при порождении процесса 3!\n");
        exit(1);
    }
    else if (pid == 0)
    {
        printf("Порождение процесса 3 (от процесса 1) PID=%d PPID=%d\n", getpid(), getppid());

        if ((pid = fork()) < 0)
        {
            printf("Ошибка при порождении процесса 6!\n");
            exit(1);
        }
        else if (pid == 0)
        {
            printf("Порождение процесса 6 (от процесса 3) PID=%d PPID=%d\n", getpid(), getppid());
            printf("Завершился процесс 6 PID=%d PPID=%d\n", getpid(), getppid());
            exit(0);
        }
        else sleep(1);

        if ((pid = fork()) < 0)
        {
            printf("Ошибка при порождении процесса 7!\n");
            exit(1);
        }
        else if (pid == 0)
        {
            printf("Порождение процесса 7 (от процесса 3) PID=%d PPID=%d\n", getpid(), getppid());
            printf("Завершился процесс 7 PID=%d PPID=%d\n", getpid(), getppid());
            exit(0);
        }
        else sleep(1);

        printf("Завершился процесс 3 PID=%d PPID=%d\n", getpid(), getppid());
        exit(0);
    }
    else sleep(1);

    return 0;
}