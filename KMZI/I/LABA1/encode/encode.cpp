#include "../libs.hh"
#include "../cardano.cpp"

int main()
{
    std::ifstream infile("input.txt"); 
    std::string to_encode;
    if (infile.is_open()) 
    {
        std::getline(infile, to_encode); 
        infile.close(); 
    }
    else
    {
        std::cerr << "Error: Unable to open file" << std::endl;
        return 1;
    }
    
    int n = ceil(sqrt(to_encode.length()));
    while(n * n > to_encode.length()) to_encode.append(std::to_string(rand() % 9));
    std::vector<std::vector<int>> grid = make_grid(n);
    std::string to_decode = encode_cardano(grid, to_encode);

    std::ofstream outfile("encode.txt"); 
    outfile << to_decode; 
    outfile.close(); 
}