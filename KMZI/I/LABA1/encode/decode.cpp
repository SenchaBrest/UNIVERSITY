#include "../libs.hh"
#include "../cardano.cpp"

int main()
{
    std::ifstream infile("encode.txt"); 
    std::string to_decode;
    if (infile.is_open()) 
    {
        std::getline(infile, to_decode); 
        infile.close(); 
    }
    else
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        return 1;
    }
    
    int n = ceil(sqrt(to_decode.length()));
    std::vector<std::vector<int>> grid = make_grid(n);
    std::string from_decode = decode_cardano(grid, to_decode);
    
    std::ofstream outfile("output.txt"); 
    outfile << from_decode; 
    outfile.close(); 

}