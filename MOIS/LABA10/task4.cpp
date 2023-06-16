#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

std::vector<std::vector<int>> getSubsets(std::vector<int>& nums) 
{
    int n = nums.size();
    int numSubsets = pow(2, n);
    std::vector<std::vector<int>> subsets(numSubsets, std::vector<int>());

    for (int i = 0; i < numSubsets; i++) 
        for (int j = 0; j < n; j++) 
            if (i & (1 << j)) 
                subsets[i].push_back(nums[j]);
            
    return subsets;
}


std::vector<int> min_dominating_set(std::vector<std::vector<int>> &adjMatrix) 
{
    std::vector<int> nums;
    for(int i = 0; i < adjMatrix.size(); i++)
        nums.push_back(i);
    std::vector<std::vector<int>> subsets = getSubsets(nums);

    int n = adjMatrix.size();
    int m = subsets.size();
    std::vector<int> minSet;
    int minSize = n + 1;
    for (int i = 0; i < m; i++) 
    {
        std::vector<int> subset = subsets[i];
        int subsetSize = subset.size();
        bool isDominating = true;
        for (int j = 0; j < n; j++) 
        {
            if (find(subset.begin(), subset.end(), j) == subset.end()) 
            {
                bool isAdjacent = false;
                for (int k = 0; k < subsetSize; k++) 
                {
                    if (adjMatrix[j][subset[k]] == 1) 
                    {
                        isAdjacent = true;
                        break;
                    }
                }
                if (!isAdjacent) 
                {
                    isDominating = false;
                    break;
                }
            }
        }
        if (isDominating && subsetSize < minSize) 
        {
            minSet = subset;
            minSize = subsetSize;
        }
    }
    return minSet;
}


int main() 
{
    std::vector<std::vector<int>> adjancy = {
	    {0,1,0,1,0,1,1,0},
	    {1,0,1,0,1,0,0,1},
	    {0,1,0,0,0,1,0,0},
	    {1,0,0,0,0,0,0,1},
	    {0,1,0,0,0,1,0,0},
	    {1,0,1,0,1,0,1,0},
	    {1,0,0,0,0,1,0,1},
	    {0,1,0,1,0,0,1,0}
    };

    std::vector<int> min_set = min_dominating_set(adjancy);

    std::cout << "min domination set size: " << min_set.size() << std::endl;
    std::cout << "min domination set: {";
    for (auto elem : min_set)
        std::cout << elem << " ";
    std::cout << "}";
}


