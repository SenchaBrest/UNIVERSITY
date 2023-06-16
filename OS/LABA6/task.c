#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <math.h>

#define MQ_NAME "my_fifo"

int fd_fifo;
char buf[20];

void sig_handler_parent(int signum){
    printf("Parent : Received a response signal from child \n");
    read(fd_fifo, buf, 20);
    printf("Answer: %s\r\n", buf);
}

void sig_handler_child(int signum){
    printf("Child : Received a signal from parent \n");
    read(fd_fifo, buf, 20);
    int a, b;
    sscanf(buf, "%d %d", &a, &b);
    float c = sqrt(a*a + b*b);
    float alpha = acos(a/c);
    float beta = acos(b/c);
    sprintf(buf, "%f %f", alpha, beta);
    write(fd_fifo, buf, strlen(buf));
    buf[0] = '\0';
    sleep(1);
    kill(getppid(),SIGUSR1);
}

int main(){
    pid_t pid;

    unlink(MQ_NAME);
    (void)umask(0);

    if ((mkfifo(MQ_NAME, 0666)) != 0)
    {
        perror("Невозможно создать fifo\n");
        exit(1);
    }
    if ((fd_fifo = open(MQ_NAME, O_RDWR)) == - 1)
    {
        perror("Невозможно открыть fifo\n");
        exit(1);
    }
    
    if ((pid = fork())<0){
        printf("Fork Failed\n");
        exit(1);
    }
    /* Child Process */
    else if(pid == 0){
        signal(SIGUSR1,sig_handler_child); 
        printf("Child: waiting for signal\n");
        pause();
    }
    /* Parent Process */
    else{
        signal(SIGUSR1,sig_handler_parent);
        sleep(1);
        sprintf(buf, "%d %d", 3, 4);
        write(fd_fifo, buf, strlen(buf));
        buf[0] = '\0';
        printf("Parent: sending signal to Child\n");
        kill(pid,SIGUSR1);
        printf("Parent: waiting for response\n");
        pause();
    }
    return 0;
}

/*Child: waiting for signal
Parent: sending signal to Child
Parent: waiting for response
Child : Received a signal from parent 
Parent : Received a response signal from child 
Answer: 0.927295 0.643501
*/