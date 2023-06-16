#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections.txt";
	VEC1 nodes = c.reading_file(file_path);
	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.adjancy(nodes, max_node);

	// find Hamiltonian Cycle 
    queue q;
    alg search;
    q = search.findHamiltonianCycle(adjacencyMatrix);
    q.print();
}