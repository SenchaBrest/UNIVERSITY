#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>

class RD_WR_Console
{
private:
    std::string str;
public:
    RD_WR_Console() {}
    RD_WR_Console(std::string str) : str(str) {}
    void read()
    {
        std::cout << "Enter string: ";
        std::getline(std::cin, str);
    }
    void write()
    {
        puts(str.c_str());
    }
};

class RD_WR_File
{
private:
    std::string str;
public:
    RD_WR_File() {}
    RD_WR_File(std::string str) : str(str) {}
    void read()
    {
        std::cout << std::endl;
        std::ifstream file("file1.txt");
        getline(file, str);
        std::cout << std::left << std::setw(10) << str;
        file.close();
    }
    void write()
    {
        std::ofstream file("file1.txt");
        file << str;
        file.close();
    }
};

class RD_WR_ARRAY_File
{
private:
    std::string str[3];
public:
    RD_WR_ARRAY_File() {}
    RD_WR_ARRAY_File(std::string str[3])
    {
        for (int i = 0; i < 3; i++)
            this->str[i] = str[i];
    }
    void read()
    {
        std::ifstream file("file2.txt");
        std::cout << std::endl;
        for (int i = 0; i < 3; i++)
        {
            getline(file, str[i]);
            std::cout << std::left << std::setw(10) << str[i];
        }
        file.close();
    }
    void write()
    {
        std::ofstream file("file2.txt");
        for (int i = 0; i < 3; i++)
        {
            file << str[i] << std::endl;
        }
        file.close();
    }
};

int main()
{
    RD_WR_Console rd_wr_console;
    RD_WR_File rd_wr_file("2");
    std::string str[3] = { "3", "4", "5" };
    RD_WR_ARRAY_File rd_wr_array_file(str);
    rd_wr_console.read();
    rd_wr_console.write();
    rd_wr_file.write();
    rd_wr_file.read();
    rd_wr_array_file.write();
    rd_wr_array_file.read();
    return 0;
}
