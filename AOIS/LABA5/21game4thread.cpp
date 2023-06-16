#include <iostream>
#include <thread>
#include <fstream>
#include <vector>
#include <string>
#include <Windows.h>
#include <numeric>

using VEC1 = std::vector<int>;
HANDLE sem_r, sem1, sem2, sem_p;

void random_numbers(int num_games, VEC1& nums, bool& done1, bool& done2)
{
    for(int i = 0; i < num_games; i++) 
    {
        while (!done1)
        {
            nums.push_back(rand() % 10 + 2);
            ReleaseSemaphore(sem1, 1, NULL);
            WaitForSingleObject(sem_r, INFINITE);
        }
        while (!done2)
        {
            nums.push_back(rand() % 10 + 2);
            ReleaseSemaphore(sem2, 1, NULL);
            WaitForSingleObject(sem_r, INFINITE);
        }
        ReleaseSemaphore(sem_p, 1, NULL);
        WaitForSingleObject(sem_r, INFINITE);
        done1 = false, done2 = false;
    }
}

void player1(int num_games, VEC1& nums, VEC1& seq, bool& done)
{
    for(int i = 0; i < num_games; i++)
    {
        int n, sum = 0;
        while (true)
        {
            WaitForSingleObject(sem1, INFINITE);
            n = nums.back();
            ReleaseSemaphore(sem_r, 1, NULL);
            if (sum > 21 || (sum > 10 && rand() % 2)) break;
            sum += n;
            seq.push_back(n);
        }
        done = true;
    }
}

void player2(int num_games, VEC1& nums, VEC1& seq, bool& done)
{
    for(int i = 0; i < num_games; i++)
    {
        int n, sum = 0;
        while (true)
        {
            WaitForSingleObject(sem2, INFINITE);
            n = nums.back();
            ReleaseSemaphore(sem_r, 1, NULL);
            if (sum > 21 || (sum > 10 && rand() % 2)) break;
            sum += n;
            seq.push_back(n);
        }
        done = true;
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

void print_results(int num_games, VEC1& rand_nums, VEC1& plr1list, VEC1& plr2list, VEC1& results)
{
    std::ofstream file("results.txt");
    for (int i = 0; i < num_games; i++)
    {
        WaitForSingleObject(sem_p, INFINITE);
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
        ReleaseSemaphore(sem_r, 1, NULL);
    }
    file.close();
}

int main()
{
    srand(time(NULL));
    int num_games = 10000;
    VEC1 rand_nums, plr1list, plr2list, results = {0, 0, 0};
    bool done1 = false, done2 = false;
    sem_r = CreateSemaphore(NULL, 0, 1, NULL);
    sem1 = CreateSemaphore(NULL, 0, 1, NULL);
    sem2 = CreateSemaphore(NULL, 0, 1, NULL);
    sem_p = CreateSemaphore(NULL, 0, 1, NULL);

    std::thread t1(random_numbers, num_games, std::ref(rand_nums), std::ref(done1), std::ref(done2));
    std::thread t2(player1, num_games, std::ref(rand_nums), std::ref(plr1list), std::ref(done1));
    std::thread t3(player2, num_games, std::ref(rand_nums), std::ref(plr2list), std::ref(done2));
    std::thread t4(print_results, num_games, std::ref(rand_nums), std::ref(plr1list), std::ref(plr2list), std::ref(results));

    t1.join();
    t2.join();
    t3.join();
    t4.join();

    CloseHandle(sem_r);
    CloseHandle(sem1);
    CloseHandle(sem2);
    CloseHandle(sem_p);
    for (int i = 0; i < results.size(); i++) std::cout << i << " : " << results[i] << std::endl;
}
