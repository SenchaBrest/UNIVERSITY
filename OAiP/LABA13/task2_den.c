#define TRUE 1 

#include <stdio.h> 
#include <conio.h> 
#include <process.h> 
#include <stdlib.h> 

void BlockWriteFile(char* ,char* , unsigned , unsigned , unsigned , unsigned ); 
int* InitMatrix(unsigned ,unsigned , unsigned ); 
int* FreeMemory(unsigned , unsigned ); 
void DisplayFile( char* , char* , unsigned , unsigned , unsigned ); 

void CompareFile(char* , char* , char* , unsigned , unsigned );
void DisplayMatrix (int* , unsigned , unsigned ); 
int* SimpleMatrix(unsigned , unsigned ); 
void WorkFile( char* , char* , char* , unsigned , unsigned , unsigned ); 
int SumElemMatrix ( int* , unsigned , unsigned ); 

int main(void) { 
    unsigned k, l, n, m ; 
    char FileName1 [20], FileName2 [20]; 
    while(TRUE) { 
        printf("\nEnter k number of matrixs:\n"); 
        scanf("%u",&k); 
        printf("\nEnter n, m, l dimentions of matrixs:\n"); 
        scanf("%u%u%u",&n,&m,&l); 
        if ( (k > 0) && (n > 0) && (m > 0) && (l > 0) ) break; 
        printf("\nNumber is incorrect!!! Try again!!!\n"); 
    } 
    printf("\nEnter the name of file: \n"); 
    scanf("%s",FileName1); 

    BlockWriteFile(FileName1, "wb", k, n, m, l); 
    printf("\nThe contents of file <<%s>>:\n", FileName1); 
    DisplayFile(FileName1, "rb", n, m, l); 

    printf("\nEnter the name of file: \n"); 
    scanf("%s",FileName2); 
    WorkFile(FileName1, FileName2, "a+b", n, m, l);
     
    printf("\nThe contents of file <<%s>>:\n",FileName2); 
    DisplayFile(FileName2, "rb", n, 0, l);

    printf("\n Press any key to exit..."); 
    getch(); 
    return 0; 
} 

int* InitMatrix(unsigned l, unsigned n, unsigned m) { 
    unsigned i; 
    int* Pointer = (int*)malloc(n*m*sizeof(int)); 
    for( i = 0; i < n * m; i++) { 
        Pointer[i] = rand()%10; // l + 1;
    } 
    return Pointer; 
} 

int* FreeMemory(unsigned n, unsigned m) { 
    int* Pointer = (int*)malloc(n*m*sizeof(int)); 
    return Pointer; 
} 

void BlockWriteFile(char* String, char* Mode, unsigned k, unsigned n, unsigned m, unsigned l) { 
    int BufSize1 = sizeof(int) * n * m; 
    int* Pointer1 = (int*)malloc(BufSize1); 
    int BufSize2 = sizeof(int) * m * l; 
    int* Pointer2 = (int*)malloc(BufSize2); 
    unsigned i; 
    FILE* FilePointer= fopen(String, Mode); 
    if (FilePointer== NULL) { 
        printf("Can't open file to write."); 
        getch(); 
        abort(); 
    } 

    for ( i = 0; i < k; i++ ) { 
        Pointer1 = InitMatrix(i, n, m); 
        fwrite(Pointer1, BufSize1,1, FilePointer); 
        Pointer2 = InitMatrix(i, m, l); 
        fwrite(Pointer2, BufSize2,1, FilePointer); 
    } 
    fclose(FilePointer); 
    free(Pointer1);
    free(Pointer2); 
} 

void DisplayFile(char* String, char* Mode, unsigned n, unsigned m,  unsigned l) { 
    if  (m == 0) {
        int BufSize = sizeof(int)*n*l, Sector = 0; 
        int* Pointer = FreeMemory(n, l); 
        FILE* FilePointer= fopen(String, Mode); 

        if ( FilePointer== NULL) { 
            printf("\nCan't open file to read."); 
            getch(); 
            abort(); 
        } 

        while(fread(Pointer,BufSize,1, FilePointer) != 0) { 
            printf("\n %d's matrix \n",(Sector + 1)); 
            DisplayMatrix(Pointer, n, l); 
            Sector++; 
        } 
        fclose(FilePointer); 
        free(Pointer); 
    }
    else {
        int BufSize1 = sizeof(int)*n*m, Sector = 0; 
        int* Pointer1 = FreeMemory(n, m);
        int BufSize2 = sizeof(int)*m*l; 
        int* Pointer2 = FreeMemory(m, l); 
        FILE* FilePointer= fopen(String, Mode); 
        if ( FilePointer== NULL) { 
            printf("\nCan't open file to read."); 
            getch(); 
            abort(); 
        } 

        while(fread(Pointer1,BufSize1,1, FilePointer) != 0) { 
            printf("\n %d's struct \n",(Sector + 1)); 
            DisplayMatrix(Pointer1, n, m);
            printf("\n");
            fread(Pointer2,BufSize2,1, FilePointer);
            DisplayMatrix(Pointer2, m, l); 
            Sector++; 
        } 
        fclose(FilePointer); 
        free(Pointer1);
        free(Pointer2);
    }
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

void WorkFile(char* String1, char* String2, char* Mode, unsigned n, unsigned m, unsigned l) { 
    int* Pointer1 = FreeMemory(n, m); 
    int BufSize1 = sizeof(int)*n*m; 
    int* Pointer2 = FreeMemory(m, l); 
    int BufSize2 = sizeof(int)*m*l;
    int* Pointer3 = FreeMemory(n, l); 
    int BufSize3 = sizeof(int)*n*l; 
    
    FILE* FilePointer1= fopen(String1, Mode); 
    if ( FilePointer1== NULL) { 
        printf("Can't open file to read."); 
        getch(); 
        abort(); 
    } 
    FILE* FilePointer2= fopen(String2, Mode); 
    if ( FilePointer2== NULL) { 
        printf("Can't open file to read."); 
        getch(); 
        abort(); 
    } 
    
    while(fread(Pointer1, BufSize1,1,FilePointer1) + fread(Pointer2, BufSize2,1,FilePointer1) != 0) { 
        int s;
        for(unsigned i = 0; i < n; i++) { 
            for(unsigned j = 0; j < l; j++) { 
                s = 0;
                for (unsigned k = 0; k < m; k++) {
                    s += (*(Pointer1 + i * m + k)) * (*(Pointer2 + k * l + j));
                }
                *(Pointer3 + i*l + j) = s; 
            }
        } 
        fwrite(Pointer3, BufSize3,1, FilePointer2);     
    }
    fclose(FilePointer1); 
    fclose(FilePointer2); 
    free(Pointer1); 
    free(Pointer2); 
    free(Pointer3); 
} 