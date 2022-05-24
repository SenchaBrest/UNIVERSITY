#define TRUE 1 

#include <stdio.h> 
#include <conio.h> 
#include <process.h> 
#include <stdlib.h> 

void BlockWriteFile(char* ,char* , unsigned , unsigned , unsigned ); 
int* InitMatrix(unsigned ,unsigned , unsigned ); 
int* FreeMemory(unsigned , unsigned ); 
void DisplayFile( char* , char* , unsigned , unsigned ); 
void CompareFile(char* , char* , char* , unsigned , unsigned );
void DisplayMatrix (int* , unsigned , unsigned ); 

int main(void) { 
    unsigned k, l, n, m ; 
    char FileName1 [20], FileName2 [20]; 
    while(TRUE) { 
        printf("\nEnter k number of matrixs:\n"); 
        scanf("%u",&k); 
        printf("\nEnter n, m dimentions of matrixs:\n"); 
        scanf("%u%u",&n,&m); 
        if ( (k > 0) && (n > 0) && (m > 0) ) break; 
        printf("\nNumber is incorrect!!! Try again!!!\n"); 
    } 
    printf("\nEnter the name of file: \n"); 
    scanf("%s",FileName1); 

    BlockWriteFile(FileName1, "wb", k, n, m); 
    printf("\nThe contents of file <<%s>>:\n",FileName1); 
    DisplayFile(FileName1, "rb", n, m); 

    printf("\nEnter l number of matrixs:\n"); 
    scanf("%u",&l); 
    printf("\nEnter the name of file: \n"); 
    scanf("%s",FileName2); 

    BlockWriteFile(FileName2, "wb", l, n, m); 
    printf("\nThe contents of file <<%s>>:\n",FileName2); 
    DisplayFile(FileName2, "rb", n, m);

    CompareFile(FileName1, FileName2, "a+b", n, m); 

    printf("\nThe contents of file <<%s>>:\n",FileName1); 
    DisplayFile(FileName1, "rb", n, m); 
    printf("\nThe contents of file <<%s>>:\n",FileName2); 
    DisplayFile(FileName2, "rb", n, m);

    printf("\n Press any key to exit..."); 
    getch(); 
    return 0; 
} 

int* InitMatrix(unsigned l, unsigned n, unsigned m) { 
    unsigned i; 
    int* Pointer = (int*)malloc(n*m*sizeof(int)); 
    for( i = 0; i < n * m; i++) { 
        Pointer[i] = l + 1;//rand()%10; 
    } 
    return Pointer; 
} 

int* FreeMemory(unsigned n, unsigned m) { 
    int* Pointer = (int*)malloc(n*m*sizeof(int)); 
    return Pointer; 
} 

void BlockWriteFile(char* String, char* Mode, unsigned k, unsigned n, unsigned m) { 
    int BufSize = sizeof(int) * n * m; 
    int* Pointer = (int*)malloc(BufSize); 
    unsigned i; 
    FILE* FilePointer= fopen(String, Mode); 
    if (FilePointer== NULL) { 
        printf("Can't open file to write."); 
        getch(); 
        abort(); 
    } 

    for ( i = 0; i < k; i++ ) { 
        Pointer = InitMatrix(i, n, m); 
        fwrite(Pointer, BufSize,1, FilePointer); 
    } 
    fclose(FilePointer); 
    free(Pointer); 
} 

void DisplayFile(char* String, char* Mode, unsigned n, unsigned m) { 
    int BufSize = sizeof(int)*n*m, Sector = 0; 
    int* Pointer = FreeMemory(n, m); 
    FILE* FilePointer= fopen(String, Mode); 

    if ( FilePointer== NULL) { 
        printf("\nCan't open file to read."); 
        getch(); 
        abort(); 
    } 

    while(fread(Pointer,BufSize,1, FilePointer) != 0) { 
        printf("\n %d's matrix \n",(Sector + 1)); 
        DisplayMatrix(Pointer, n, m); 
        Sector++; 
    } 
    fclose(FilePointer); 
    free(Pointer); 
} 

void CompareFile(char* String1, char* String2, char* Mode, unsigned n, unsigned m) { 
    int BufSize = sizeof(int)*n*m;
    int* Pointer1 = FreeMemory(n, m); 
    int* Pointer2 = FreeMemory(n, m); 

    FILE* FilePointer1= fopen(String1, Mode); 
    if ( FilePointer1== NULL) { 
        printf("\nCan't open file to read."); 
        getch(); 
        abort(); 
    } 
    FILE* FilePointer2= fopen(String2, Mode); 
    if ( FilePointer2== NULL) { 
        printf("\nCan't open file to read."); 
        getch(); 
        abort(); 
    } 
    
    int flagSmall = 0, flagBig;
    while(fread(Pointer1,BufSize,1, FilePointer1) != 0 ) {
        fseek(FilePointer2,0,SEEK_SET);
        while(fread(Pointer2,BufSize,1, FilePointer2) != 0 ) {
            unsigned i, j; 
            for( i = 0; i < n; i++) { 
                for( j = 0; j < m; j++) {
                    if (*(Pointer2 + i * m + j) != *(Pointer1 + i * m + j)) {
                        flagSmall += 1;
                    }
                }
            }
            if (flagSmall > 0) {
                flagBig = 0;
            }
            else {
                flagBig = 1;
            }
            flagSmall = 0;
        } 
        if (flagBig == 0) {
            fwrite(Pointer1, BufSize,1, FilePointer2);
        }
    } 
    
    fclose(FilePointer1); 
    fclose(FilePointer2); 
    free(Pointer1);
    free(Pointer2); 
} 

void DisplayMatrix(int* Pointer, unsigned n, unsigned m) { 
    unsigned i, j; 
    for( i = 0; i < n; i++) { 
        for( j = 0; j < m; j++) {
            printf("%4d",*(Pointer + i * m + j)); 
        }
        printf("\n"); 
    } 
} 