#include "libs.hh"

struct Seg 
{
    char Symbol;
    double Left;
    double Right;
};

std::vector<Seg> DefineSeg(std::string letters, std::vector<double> probabilities) 
{
    int m = letters.length();
    std::vector<Seg> seg(m);
    double l = 0;
    for (int i = 0; i < m; i++) 
    {
        seg[i].Left = l;
        seg[i].Right = l + probabilities[i];
        seg[i].Symbol = letters[i];
        l = seg[i].Right;
    }
    return seg;
}

double ArithmeticEncoding(std::string letters, std::vector<double> probabilities, std::string str) 
{
    auto seg = DefineSeg(letters, probabilities);
    double left = 0, right = 1;
    for (int i = 0; i < str.length(); i++) 
    {
        int symb = find(letters.begin(), letters.end(), str[i]) - letters.begin();
        double newRight = left + (right - left) * seg[symb].Right;
        double newLeft = left + (right - left) * seg[symb].Left;
        left = newLeft;
        right = newRight;
    }
    return (left + right) / 2;
}

std::string ArithmeticDecoding(std::string letters, std::vector<double> probabilities, double code, int n) 
{
    auto seg = DefineSeg(letters, probabilities);
    std::string str = "";
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < letters.length(); j++) 
        {
            if (code >= seg[j].Left && code < seg[j].Right) 
            {
                str += seg[j].Symbol;
                code = (code - seg[j].Left) / (seg[j].Right - seg[j].Left);
                break;
            }
        }
    }
    return str;
}

std::vector<double> FindProbability(std::string str, std::string letters) 
{
    std::vector<double> probabilities;
    for (char c : letters) 
    {
        auto match = std::count(str.begin(), str.end(), c);
        probabilities.push_back((double)match / str.length());
    }
    return probabilities;
}

// int main()
// {
//     std::string to_compress = "hello world!";
//     std::string letters = "abcdefghijklmnopqrstuvwxyz! ,.";
//     auto probability = FindProbability(to_compress, letters);
//     double to_uncompress = ArithmeticEncoding(letters, probability, to_compress);
//     std::cout << "to_compress: " << to_uncompress << std::endl;

//     std::string from_uncompress = ArithmeticDecoding(letters, probability, to_uncompress, to_compress.length());
//     std::cout << "from_uncompress: " << from_uncompress << std::endl;
// }