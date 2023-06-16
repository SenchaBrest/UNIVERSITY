#include "../graph_LIB.hh"

int main()
{
	convert c;
	std::string file_path = "connections2.txt";
	VEC1 nodes = c.reading_file(file_path);
	int max_node = c.count_of_nodes(nodes);
	VEC2 adjacencyMatrix = c.adjancy(nodes, max_node);
    VEC2 bufferMatrix = adjacencyMatrix;

	alg search;
   	VEC1 visited(max_node);
    int count;
    count = search.conCompBFS(adjacencyMatrix);
    
    int k;
    VEC1 articulationPoints;
    for (int i = 0; i < max_node; i++)
    {
        for (int j = 0; j < bufferMatrix.size(); j++)
        {
            bufferMatrix[j].erase(bufferMatrix[j].begin() + i);
        }
        bufferMatrix.erase(bufferMatrix.begin() + i);

        k = search.conCompBFS(bufferMatrix);
        if (k > count)
        {
            articulationPoints.push_back(i);
        }
        bufferMatrix = adjacencyMatrix;
    }

    std::cout << "Articulation points: ";
    for (int i = 0; i < articulationPoints.size(); i++)
    {
        std::cout << articulationPoints[i] + 1 << " ";
    }

    VEC2 bridges;
    VEC1 vis(max_node);
    for (int i = 0; i < articulationPoints.size(); i++)
    {
        for (int j = 0; j < max_node; j++)
        {
            bufferMatrix[articulationPoints[i]][j] = 0;
            bufferMatrix[j][articulationPoints[i]] = 0;

            k = search.conCompBFS(bufferMatrix);
            if (k > count)
            {
                bridges.push_back( {articulationPoints[i], j} );
                vis[articulationPoints[i]] = 1;
                vis[j] = 1;
            }
            bufferMatrix = adjacencyMatrix;
        }
    }

    for (int i = 0; i < bridges.size(); i++)
    {
        for (int j = 0; j < bridges.size(); j++)
        {
            if (bridges[i][0] == bridges[j][1] && bridges[i][1] == bridges[j][0])
            {
                bridges.erase(bridges.begin() + j);
            }
        }
    }

    std::cout << "\nBridges: ";
    for (int i = 0; i < bridges.size(); i++)
    {
        std::cout << "(" << bridges[i][0] + 1 << ", " << bridges[i][1] + 1 << ") ";
    }
}