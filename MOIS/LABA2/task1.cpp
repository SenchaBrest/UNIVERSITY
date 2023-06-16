#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections.txt";
	VEC1 nodes = c.reading_file(file_path);
	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.adjancy(nodes, max_node);

	// first requirement
	alg search;
    if (search.conCompBFS(adjacencyMatrix) != 1)
    {
        std::cout << "The graph not coherent";
        exit(0);
    }

    // second requirement
    VEC1 degrees(max_node);
    for (int i = 0; i < max_node; i++)
    {
        for (int j = 0; j < max_node; j++)
        {
            if (adjacencyMatrix[i][j])
            {
                degrees[i]++;
            }
        } 
    }
    for (int i = 0; i < max_node; i++)
    {
        if (degrees[i] % 2 != 0)
        {
            std::cout << "The graph not Eulerian";
            exit(0);
        }
    }

    // find the Eulerian cycle
    VEC1 cycle;
    cycle = search.findEulerianCycle(adjacencyMatrix);
    std::cout << "The cycle is: ";
    for (int i = cycle.size() - 1; i >= 0; i--)
    {
        std::cout << cycle[i] + 1;
    }
}