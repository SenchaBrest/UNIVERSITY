#include <iostream>
#include <string.h>

class pSTRING
{
private:
    char *pSTR;
    int length;
public:
    pSTRING()
    {
        pSTR = new char[1];
        pSTR[0] = '\0';
        length = 0;
    }
    pSTRING(const char *str)
    {
        length = strlen(str);
        pSTR = new char[length + 1];
        strcpy(pSTR, str);
    }
    pSTRING(const pSTRING &str)
    {
        length = str.length;
        pSTR = new char[length + 1];
        strcpy(pSTR, str.pSTR);
    }
    ~pSTRING()
    {
        delete [] pSTR;
    }
    void SET(const char *str)
    {
        delete [] pSTR;
        length = strlen(str);
        pSTR = new char[length + 1];
        strcpy(pSTR, str);
    }
    char* GET()
    {
        return pSTR;
    }
    void SHOW()
    {
        std::cout << pSTR << std::endl;
    }
    int SIZE()
    {
        return length;
    }
    bool EMPTY()
    {
        return length == 0;
    }
    pSTRING &ASSIGN(const pSTRING &str)
    {
        if (this == &str)
            return *this;
        delete [] pSTR;
        length = str.length;
        pSTR = new char[length + 1];
        strcpy(pSTR, str.pSTR);
        return *this;
    }
    pSTRING &operator=(const pSTRING &str)
    {
        return ASSIGN(str);
    }
};

int main()
{
    pSTRING str1("Hello");
    pSTRING str2(str1);
    str1.SHOW();
    str2.SHOW();
    std::cout << str1.SIZE() << std::endl;
    std::cout << str2.SIZE() << std::endl;
    std::cout << str1.EMPTY() << std::endl;
    std::cout << str2.EMPTY() << std::endl;
    str1.SHOW();
    str1 = str2;
    str1.SHOW();

    pSTRING str3;
    str3.SET("World");
    char *p = str3.GET();
    while(*p)
    {
        std::cout << *p;
        p++;
    }
    return 0;
}