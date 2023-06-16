#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

int k = 0;

void print_array(int arr[], int n) 
{
    for (int i = 0; i < n; i++) 
        std::cout << arr[i] << " ";
    std::cout << std::endl;
}

void generate_permutations(int arr[], int n) 
{
    k = 0;
    std::sort(arr, arr + n);
    while (true) 
    {
        print_array(arr, n);

        int i = n - 2;
        while (i >= 0 && arr[i] >= arr[i+1])
            i--;
        if (i < 0)
            break;
        int j = n - 1;
        while (arr[i] >= arr[j])
            j--;
        std::swap(arr[i], arr[j]);
        std::reverse(arr + i + 1, arr + n);
        k++;
    }
}

std::vector<std::vector<int>> generate_permutations_from_N_to_M(int n, int m)
{
    k = 0;
    std::vector<std::vector<int>> res;
    std::vector<int> perm(n);
    for (int i = 0; i < n; i++)
        perm[i] = i;

    int count_perm = 0;
    do 
    {
        int count = 0;
        for (int i = 0; i < n; i++)
            if (perm[i] == i)
                count++;
        if (count == m) 
        {
            res.push_back(perm);
            count_perm+=1;
        }
    } while (next_permutation(perm.begin(), perm.end()));
    k++;
    return res;
}

int main(int argc, char** argv) 
{
    int choice = atoi(argv[1]);
    int num = atoi(argv[2]);
    std::vector<std::pair<int, double>> time;
    if (choice == 1)
    {
        for(int j = 2; j <= num; j++)
        {
            auto T1 = std::chrono::high_resolution_clock::now();

            int arr[j];
            for(int i = 1; i <=j; i++)
                arr[i - 1] = i;

            generate_permutations(arr,j);

            auto T2 = std::chrono::high_resolution_clock::now();
            auto duration1 = std::chrono::duration_cast<std::chrono::microseconds>(T2 - T1).count();
            std::cout << "Lead time: " << (double)duration1/1000000 << " seconds" << std::endl;
            time.push_back({k, (double)duration1 / 1000000});
        }
        for(int i = 0; i < num - 1; i++)
            std::cout << "amount of elements: "<< time[i].first << 
            " program running time: "<< time[i].second << std::endl;
    }
    else if (choice == 2)
    {
        for(int j = 3; j <= num; j++)
        {
            auto T1 = std::chrono::high_resolution_clock::now();

            int  m = 1;
            std::vector<std::vector<int>> perms = generate_permutations_from_N_to_M(j, m);
            for (auto perm : perms) 
            {
                for (auto elem : perm)
                    std::cout << elem + 1 << " ";
                std::cout << std::endl;
                k++;
            }

            auto T2 = std::chrono::high_resolution_clock::now();
            auto duration1 = std::chrono::duration_cast<std::chrono::microseconds>(T2 - T1).count();
            std::cout << "Lead time: " << (double)duration1/1000000 << " seconds" << std::endl;
            time.push_back({k, (double)duration1 / 1000000});
        }
        for(int i = 0; i < num - 2; i++)
            std::cout << "amount of elements: "<< time[i].first << 
            " program running time: "<< time[i].second << std::endl;
    }
    else
    {
        std::cout << "Invalid Argument." << std::endl;
    }
}