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
    char *begin, *end;

    while ((read(0, str, size)) > 0)
    {   
        begin = str;
        end = strstr(str, "\n");
        while (end)
        {
            if (isdigit(*begin))
            {   
                for (int i = begin - str; i < end - str; i++)
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
                write(1, begin, end - begin + 1);
            }
            begin = end + 1;
            end = strstr(end + 1, "\n");
        }
    }
    return 0;
}