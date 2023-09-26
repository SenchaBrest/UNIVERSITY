#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "time.h"
#include <vector>

int isprime(int num)
{
    if ((num * num) % 24 == 1) return true;
    if (num == 2 || num == 3) return true;
    return false;
}

int gcd(int a, int b) 
{
    return b == 0 ? a : gcd(b, a % b);
}

int pollard_rho(int n)
{
    if(n % 2 == 0) return 2;
    int x =  rand() % n + 1;
    int c = rand() % n + 1;
    int y = x;
    int g = 1;

    while(g == 1)
    {
        x = ((x * x) % n + c) % n;    
        y = ((y * y) % n + c) % n;
        y = ((y * y) % n + c) % n;
        g = gcd(abs(y - x), n);
    }
    return g;
}

void factorize_r_polard(int n, std::vector<int>& factors)
{
    if(n == 1) return;
    if(isprime(n))
    {
        factors.push_back(n);
        return;
    }
    int divisor = pollard_rho(n);
    factorize_r_polard(divisor, factors);
    factorize_r_polard(n / divisor, factors);
}

void factorize_prime(int n, std::vector<int>& factors, std::vector<int>& divisors) 
{
    for (int i = 0; i < divisors.size(); i++) 
    {
        int divisor = divisors[i];
        while (n % divisor == 0) 
        {
            factors.push_back(divisor);
            n /= divisor;
        }
    }
    if(n > 1) factors.push_back(n);
}

void factorize_combine(int n, std::vector<int>& factors, std::vector<int>& divisors)
{
    if(isprime(n))
    {
        factors.push_back(n);
        return;
    }

    for (int i = 0; i < divisors.size(); i++) 
    {
        int divisor = divisors[i];
        while (n % divisor == 0) 
        {
            factors.push_back(divisor);
            n /= divisor;
        }
    }

    if (n > 1) 
    {
        srand(time(NULL));
        int divisor = pollard_rho(n);
        factorize_r_polard(divisor, factors);
        factorize_r_polard(n / divisor, factors);
    }
}

int main(int argc, char** argv)
{
    std::vector<int> factors;

    std::vector<int> divisors = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 
        41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
        97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
        197, 199, 211, 223, 227, 229, 233, 239, 241, 251
    };

    int choice = std::atoi(argv[1]);
	int n = 1234567890;
    srand(time(NULL));
    
    if(choice == 1) factorize_prime(n, factors, divisors);
    if(choice == 2) factorize_r_polard(n, factors);
    if(choice == 3) factorize_combine(n, factors, divisors);

    for (int i = 0; i < factors.size(); ++i)
    {
        printf("%d ", factors[i] );
    }
    printf("\n");
	return 0;
}