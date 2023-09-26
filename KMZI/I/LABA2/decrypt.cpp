#include "lib.hh"

int main()
{
    std::string input_name = "encrypt.txt", output_name = "message2.txt";
    std::string cipher_text, key;
    
    std::ifstream inputfile(input_name);
    if (inputfile.is_open()) 
    {
        getline(inputfile, cipher_text);
        getline(inputfile, key);
        inputfile.close();
    } else std::cout << "Unable to open file " << input_name << std::endl;

    std::ofstream outputFile(output_name);
    if (outputFile.is_open()) 
    {        
        outputFile << DeCode(decrypt(cipher_text, key), key, 4) << std::endl;
        outputFile << key << std::endl;
        outputFile.close();
    } else std::cout << "Unable to open file " << output_name << std::endl;
}
