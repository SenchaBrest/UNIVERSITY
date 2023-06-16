#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>

# define size 10000

int main()
{
    char str[size];

    FILE * f = fopen("test.txt","r");
    if(!f)
        printf("Error open test.txt\n");
    else
    {
        while(fgets(str,size,f))
        {
            if (isdigit(*str))
            {   
                for (int i = 0; i < strlen(str); i++)
                {
                    if (str[i] == 'X')
                    {
                        str[i] = 'Y';
                    }
                    if (str[i] == 'x')
                    {
                        str[i] = 'y';
                    }
                }
                write(1, str, strlen(str));
            }
        }
        
    }
    fclose(f);
    return 0;
}