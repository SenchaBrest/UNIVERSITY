#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>
#include <fstream>

char fo(char subblock, std::string key, int round)
{
    return (subblock * key[round]) % static_cast<char>(pow(2, round)+1);
}

std::string DeCode(std::string mes, std::string key, int n)
{
    char temp = '0', l = '0', r = '0';
    for (int desc = 0; desc < mes.size(); desc += 10)
    {
        l = mes[desc];
        r = mes[desc + 1];
        for (int i = n-1; i >= 0; --i)
        {
            temp = l ^ fo(r, key, i);
            l = r;
            r = temp;
        }
        mes[desc] = l;
        mes[desc + 1] = r;
    }
    return mes;
}

std::string Code(std::string mes, std::string key, int n)
{
    char temp = '0', l = '0', r = '0';
    for (int desc = 0; desc < mes.size(); desc += 10)
    {
        l = mes[desc];
        r = mes[desc + 1];
        for (int i = 0; i < n; ++i)
        {
            temp = r ^ fo(l, key, i);
            r = l;
            l = temp;
        }
        mes[desc] = l;
        mes[desc + 1] = r;
    }
    return mes;
}

std::string encrypt(std::string plaintext, std::string key)
{
    std::string ciphertext = plaintext;
    int n = plaintext.size();

    std::vector<int> table(key.size());
    for (int i = 0; i < key.size(); i++) table[i] = i;
    std::sort(table.begin(), table.end(), [&](int i, int j) {return key[i] < key[j];});
    
    for (int i = 0; i < n; i++)
    {
        int j = i % key.size();
        int k = i / key.size() * key.size() + table[j];
        ciphertext[k] = plaintext[i];
    }
    
    return ciphertext;
}

std::string decrypt(std::string ciphertext, std::string key)
{
    std::string plaintext = ciphertext;
    int n = ciphertext.size();
    
    std::vector<int> table(key.size());
    for (int i = 0; i < key.size(); i++) table[i] = i;
    std::sort(table.begin(), table.end(), [&](int i, int j) {return key[i] < key[j];});
    std::vector<int> inv_table(key.size());
    for (int i = 0; i < key.size(); i++) inv_table[table[i]] = i;
    
    for (int i = 0; i < n; i++)
    {
        int j = i % key.size();
        int k = i / key.size() * key.size() + inv_table[j];
        plaintext[k] = ciphertext[i];
    }
    
    return plaintext;
}