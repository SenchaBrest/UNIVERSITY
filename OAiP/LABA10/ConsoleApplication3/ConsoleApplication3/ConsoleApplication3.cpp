#include <iostream>

int fib1(int N, int &k) {

    ++k;
    if (N == 1 or N == 2) {
        return 1;
    }
    
    return (fib1(N - 2, k) + fib1(N - 1, k));
    
}
int main() {

    int A = 1, B = 2, C = 3, D = 4, E = 5;
    int k; 
    k = 0;
    std::cout << fib1(A, k);
    std::cout << "; count of calls = " << k << std::endl;
    
    k = 0;
    std::cout << fib1(B, k);
    std::cout << "; count of calls = " << k << std::endl;
    
    k = 0;
    std::cout << fib1(C, k);
    std::cout << "; count of calls = " << k << std::endl;
    
    k = 0;
    std::cout << fib1(D,k);
    std::cout << "; count of calls = " << k << std::endl;
    
    k = 0;
    std::cout << fib1(E,k);
    std::cout << "; count of calls = " << k << std::endl;
    
}

