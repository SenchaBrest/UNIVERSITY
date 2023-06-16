#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections1.txt";
	VEC1 nodes = c.reading_file(file_path);

	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.di_adjancy(nodes, max_node);

    alg search;
    
    VEC1 n_comps;
    for (int i = 0; i < max_node; i++)
    {
        n_comps.push_back(search.conCompDFS_strong(adjacencyMatrix, i));
    }
    int max_n_comp = *max_element(n_comps.begin(), n_comps.end());
    int index = std::distance(n_comps.begin(), std::find(n_comps.begin(), n_comps.end(), max_n_comp));

    VEC2 comps(max_n_comp);
    std::cout << "count = " << max_n_comp << std::endl;
    search.conCompDFS_strong(adjacencyMatrix, comps, index);
    for (int i = 0; i < max_n_comp; i++)
    {
        std::cout << "Component " << i + 1 << ": ";
        for (int j = 0; j < comps[i].size(); j++)
        {
            std::cout << comps[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << max_n_comp;
}