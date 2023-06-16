#include "../graph_LIB.hh"

int main()
{
    convert c;
    alg a;
    // 1 2 3 4 5 6
    // 5 4 2 6 3 1
    VEC1 perm = {5, 4, 2, 6, 3, 1};
    VEC1 nodes = perm;
    int i = 1;
    for (auto it = nodes.begin(); it != nodes.end(); it += 1) 
    {
        it = nodes.insert(it + 1, i); 
        i++;
    }

    VEC2 matrix = c.adjancy(nodes, perm.size());
    int n_comp = a.conCompDFS_strong(matrix, 0);
    VEC2 cycles(n_comp);
    a.conCompDFS_strong(matrix, cycles, 3);
    VEC1 sizes;
    int numInversions = 0, numTranspositions = 0;
    for (int i = 0; i < n_comp; i++)
    {
        sizes.push_back(cycles[i].size());
        std::cout << "Cycle " << i + 1 << ": ";
        for (int j = 0; j < cycles[i].size(); j++)
        {
            std::cout << cycles[i][j] + 1 << " ";
        }
        std::cout << std::endl;
    }

    std::cout << "Degree of substitution: " << a.lcm_n(sizes) << std::endl;

    std::cout << "Parity of substitution by transpositions: " << \
    (a.getNumTranspositions(perm) % 2 == 0) << std::endl;

    std::cout << "Parity of substitution by inversions: " << \
    (a.getNumInversions(perm, 0, perm.size() - 1) % 2 == 0) << std::endl;

}