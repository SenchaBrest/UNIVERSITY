#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections.txt";
	VEC1 nodes = c.reading_file(file_path);
	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.adjancy(nodes, max_node);

	alg search;
   	VEC1 visited(max_node);
    int count;
    count = search.conCompBFS(adjacencyMatrix);
	//searching count by BFS    
    std::cout << "BFS: count = " << count << std::endl; 
    count = search.conCompDFS(adjacencyMatrix);
	//searching count by DFS
    std::cout << "DFS: count = " << count << std::endl;
}