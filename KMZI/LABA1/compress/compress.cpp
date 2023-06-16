#include "../libs.hh"
#include "../ariphmetic.cpp"

int main()
{
    std::ifstream infile("input.txt"); 
    std::string to_compress;
    if (infile.is_open()) 
    {
        std::getline(infile, to_compress); 
        infile.close(); 
    }
    else
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        return 1;
    }

    std::string letters = "abcdefghijklmnopqrstuvwxyz! ";
    auto probability = FindProbability(to_compress, letters);
    double to_uncompress = ArithmeticEncoding(letters, probability, to_compress);

    std::ofstream outfile("compress.txt"); 
    outfile << to_uncompress; 
    outfile.close(); 

    std::ofstream probfile("probabilities.txt");
    probfile << to_compress.length() << std::endl;
    for (const auto& p : probability)
        probfile << p << std::endl; 
    probfile.close();
}
