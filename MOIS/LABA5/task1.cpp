#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections.txt";
	VEC1 nodes = c.reading_file(file_path);
	file_path = "weights.txt";
	VEC1 weights = c.reading_file(file_path);

	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.adjancy(nodes, weights, max_node);

    alg search;
    VEC2 tree;
    tree = search.Prim(adjacencyMatrix);
    VEC1 couple = c.couple_from_adjancy(tree);

    c.print(couple);
}