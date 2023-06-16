#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "time.h"
#include "bignumber.h"
#include <vector>

using big = pr0crustes::BigNumber;

big random(int n)
{
    big b;
    return b.randomBigNumber(n);
}

bool isprime(big num)
{
    if ((num * num) % 24 == 1) return true;
    if (num == 2 || num == 3) return true;
    return false;
}

big gcd(big a, big b) 
{
    return b == 0 ? a : gcd(b, a % b);
}

big pollard_rho(big n)
{
    if(n % 2 == 0) return 2;
    big x = random(6) % n + 1;
    big c = random(6) % n + 1;
    big y = x;
    big g = 1;

    while(g == 1)
    {
        x = ((x * x) % n + c) % n;    
        y = ((y * y) % n + c) % n;
        y = ((y * y) % n + c) % n;
        if (y >= x) g = gcd(y - x, n);
        else gcd(x - y, n);
    }
    return g;
}

void factorize_r_polard(big n, std::vector<big>& factors)
{
    if(n == 1) return;
    if(isprime(n))
    {
        factors.push_back(n);
        return;
    }
    big divisor = pollard_rho(n);
    factorize_r_polard(divisor, factors);
    factorize_r_polard(n / divisor, factors);
}

void factorize_prime(big n, std::vector<big>& factors, std::vector<int>& divisors) 
{
    for (int i = 0; i < divisors.size(); i++) 
    {
        int divisor = divisors[i];
        while (n % (big)divisor == 0) 
        {
            factors.push_back(divisor);
            n /= (big)divisor;
        }
    }
    if(n > 1) factors.push_back(n);
}

void factorize_combine(big n, std::vector<big>& factors, std::vector<int>& divisors)
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
        big divisor = pollard_rho(n);
        factorize_r_polard(divisor, factors);
        factorize_r_polard(n / divisor, factors);
    }
}

int main(int argc, char** argv)
{
    std::vector<big> factors;

    std::vector<int> divisors = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 
        41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
        97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
        197, 199, 211, 223, 227, 229, 233, 239, 241, 251
    };

    pr0crustes::BigNumber n("1000011783");
    int choice = std::atoi(argv[1]);
    srand(time(NULL));
    
    if(choice == 1) factorize_prime(n, factors, divisors);
    if(choice == 2) factorize_r_polard(n, factors);
    if(choice == 3) factorize_combine(n, factors, divisors);

    for (int i = 0; i < factors.size(); ++i)
        std::cout << factors[i] << " ";
}