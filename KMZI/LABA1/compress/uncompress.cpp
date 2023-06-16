#include "../libs.hh"
#include "../ariphmetic.cpp"

int main()
{
    std::ifstream infile("compress.txt"); 
    std::string to_uncompress;
    if (infile.is_open()) 
    {
        std::getline(infile, to_uncompress); 
        infile.close(); 
    }
    else
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        return 1;
    }

    std::string letters = "abcdefghijklmnopqrstuvwxyz! ";

    std::ifstream probinfile("probabilities.txt");
    std::vector<double> probability;
    double prob;
    std::string len;
    probinfile >> len;
    while (probinfile >> prob) 
    {
        probability.push_back(prob);
    }
    probinfile.close(); 

    std::string from_uncompress = ArithmeticDecoding(letters, probability, std::stod(to_uncompress), std::stoi(len));

    std::ofstream outfile("output.txt"); 
    outfile << from_uncompress; 
    outfile.close(); 
}
