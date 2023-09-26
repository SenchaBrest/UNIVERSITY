#include <iostream>
#include <bitset>

class LFSR 
{
private:
    std::bitset<8> state;
    std::bitset<8> polynomial;

public:
    LFSR(std::string seed, std::string poly) 
    {
        state = std::bitset<8>(seed);
        polynomial = std::bitset<8>(poly);
    }

    bool next() 
    {
        bool output = state[0];
        bool feedback = (state & polynomial).count() % 2;
        state >>= 1; 
        state.set(7, feedback);
        return output;
    }

    std::string generate(int n) 
    {
        std::string result = "";
        for (int i = 0; i < n; i++) 
        {
            bool bit = next();
            result += std::to_string(bit);
        }
        return result;
    }

    std::string to_decimal(std::string bits) 
    {
        std::string result = "";
        for (int i = 0; i < bits.length(); i += 8) 
        {
            std::string byte_str = bits.substr(i, 8); 
            int byte_int = std::bitset<8>(byte_str).to_ulong();
            result += std::to_string(byte_int) + " ";
        }
        return result;
    }
};

int main() 
{
    std::cout << "f(x) = x ^ 7 + x + 1\n";
    LFSR lfsr1("1101011", "11000001");
    std::string bits1 = lfsr1.generate(32);
    std::string decimals1 = lfsr1.to_decimal(bits1);
    std::cout << "Generated sequence: " << bits1 << std::endl;
    std::cout << "Decimals: " << decimals1 << std::endl;

    std::cout << "f(x) = x ^ 7 + x ^ 5  + x ^ 3 + 1\n";
    LFSR lfsr2("1101011", "10010101");
    std::string bits2 = lfsr2.generate(32);
    std::string decimals2 = lfsr2.to_decimal(bits2);
    std::cout << "Generated sequence: " << bits2 << std::endl;
    std::cout << "Decimals: " << decimals2 << std::endl;

    std::cout << "f(x) = x ^ 7 + x ^ 6  + x ^ 5 + x ^ 2 + 1\n";
    LFSR lfsr3("1101011", "10100111");
    std::string bits3 = lfsr3.generate(32);
    std::string decimals3 = lfsr3.to_decimal(bits3);
    std::cout << "Generated sequence: " << bits3 << std::endl;
    std::cout << "Decimals: " << decimals3 << std::endl;
}
