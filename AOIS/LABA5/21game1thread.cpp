#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <numeric>

using VEC1 = std::vector<int>;

void player(int num_games, VEC1& nums, VEC1& seq)
{
    int n, sum = 0;
    while (true)
    {
        n = rand() % 10 + 2;
        if (sum > 21 || (sum > 10 && rand() % 2 == 0)) break;
        sum += n;
        seq.push_back(n);
    }    
}

void write_vector_to_file(const VEC1& vec, std::ofstream& file)
{
    for (auto it = vec.begin(); it != vec.end(); ++it) 
    {
        file << *it;
        if (it != vec.end() - 1) file << ",";
    }
    file << "\n";
}

void print_results(int num_games, VEC1& rand_nums, VEC1& plr1list, VEC1& plr2list, VEC1& results, std::ofstream& file)
{
    write_vector_to_file(rand_nums, file);
    write_vector_to_file(plr1list, file);
    write_vector_to_file(plr2list, file);
    int sum1 = std::accumulate(plr1list.begin(), plr1list.end(), 0);
    int sum2 = std::accumulate(plr2list.begin(), plr2list.end(), 0);
    if ((sum1 > 21 && sum2 > 21) || sum1 == sum2) 
    {
        file << 0 << std::endl;
        results[0]++;
    }
    else if ((sum1 <= 21 && sum2 > 21) || ((21 - sum1 < 21 - sum2) && sum1 <= 21 && sum2 <= 21)) 
    {
        file << 1 << std::endl;
        results[1]++;
    }
    else
    {
        file << 2 << std::endl;
        results[2]++;
    }
    rand_nums.clear();
    plr1list.clear();
    plr2list.clear();
}

int main()
{
    srand(time(NULL));
    int num_games = 100000;
    VEC1 rand_nums;
    VEC1 plr1list;
    VEC1 plr2list;
    VEC1 results = {0, 0, 0};

    std::ofstream file("results.txt");
    for(int i = 0; i < num_games; i++)
    {
        player(num_games, rand_nums, plr1list);
        player(num_games, rand_nums, plr2list);
        print_results(num_games, rand_nums, plr1list, plr2list, results, file);
    }
    file.close();
    for (int i = 0; i < results.size(); i++) std::cout << i << " : " << results[i] << std::endl;
}
