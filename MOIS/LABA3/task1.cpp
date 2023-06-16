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
    int start = 0;
    VEC1 distance;
    VEC1 path(max_node);
    
    distance = search.Dejkstra(adjacencyMatrix, start, path);
    
    VEC1 way;
    for (int i = 0; i < max_node; i++)
    {
        std::cout << std::endl << start << "->" << i << " : " << distance[i];
        std::cout << "\tPath:";
        search.thisIsTheWay(path, start, i, way);
        for (int j = 0; j < way.size(); j++)
        {
            std::cout << way[j];
        }
        way.clear();
    }
}