#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections.txt";
	VEC1 nodes = c.reading_file(file_path);
	int max_node = c.count_of_nodes(nodes);
	int n = nodes.size() / 2;
	VEC2 adjacencyMatrix = c.adjancy(nodes, max_node);
	VEC2 incidenceMatrix = c.incidence(nodes, max_node);
		
	for (int i = 0; i < max_node; i++)
	{
		for (int j = 0; j < max_node; j++)
		{
			std::cout << adjacencyMatrix[i][j];
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;

	for (int i = 0; i < max_node; i++)
	{
		for (int j = 0; j < n; j++)
		{
			std::cout << incidenceMatrix[i][j];
		}
		std::cout << std::endl;
	}
}