#include "lib.hh"

int main()
{
    std::string input_name = "message.txt", output_name = "encrypt.txt";
    std::string message, key;

    std::ifstream inputfile(input_name);
    if (inputfile.is_open()) 
    {
        getline(inputfile, message);
        getline(inputfile, key);
        inputfile.close();
    } else std::cout << "Unable to open file " << input_name << std::endl;

    std::ofstream outputFile(output_name);
    if (outputFile.is_open()) 
    {        
        outputFile << encrypt(Code(message, key, 4), key) << std::endl;
        outputFile << key << std::endl;
        outputFile.close();
    } else std::cout << "Unable to open file " << output_name << std::endl;
}