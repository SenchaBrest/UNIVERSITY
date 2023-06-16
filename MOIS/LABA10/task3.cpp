#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <string>
#include <stack>
using namespace std;
const int INF = 1e9;
vector<int> reading_file(string path){
    ifstream input_file("task3.txt");
    vector<int> numbers;

    if (input_file.is_open()) {
        string line;
        while (getline(input_file, line)) {
            // Ищем все числа в строке
            for (int i = 0; i < line.length(); i++) {
                if (isdigit(line[i])) {
                    string number_str = "";
                    while (isdigit(line[i])) {
                        number_str += line[i];
                        i++;
                    }
                    int number = stoi(number_str);
                    numbers.push_back(number);
                }
            }
        }
        input_file.close();
    }
    else {
        cout << "Не удалось открыть файл" << endl;
        
    }

    return numbers;
}


std::vector<std::vector<int>> floyd_warshall(const std::vector<std::vector<int>>& graph) {
    int n = graph.size();
    std::vector<std::vector<int>> dist(n, std::vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            dist[i][j] = graph[i][j];
        }
    }
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }
    return dist;
}

int diameter(const std::vector<std::vector<int>>& graph) {
    auto dist = floyd_warshall(graph);
    int diameter = 0;
    for (int i = 0; i < graph.size(); ++i) {
        for (int j = 0; j < graph.size(); ++j) {
            if (dist[i][j] != INF) {
                diameter = std::max(diameter, dist[i][j]);
            }
        }
    }
    return diameter;
}

std::vector<std::vector<int>> diameter_paths(const std::vector<std::vector<int>>& graph,int diameter) {
    auto dist = floyd_warshall(graph);
    std::vector<std::vector<int>> paths;
    for (int i = 0; i < graph.size(); ++i) {
        for (int j = i + 1; j < graph.size(); ++j) {
            if (dist[i][j] == diameter) {
                std::vector<int> path = {i, j};
                while (true) {
                    int k = -1;
                    for (int l = 0; l < graph.size(); ++l) {
                        if (l != path[path.size() - 2] && graph[path[path.size() - 2]][l] != INF && dist[l][j] == dist[path[path.size() - 2]][j] - graph[path[path.size() - 2]][l]) {
                            k = l;
                            break;
                        }
                    }
                    if (k == -1) {
                        break;
                    }
                    path.insert(path.end() - 1, k);
                }
                paths.push_back(path);
            }
        }
    }
    return paths;
}
int radius_graph(const std::vector<std::vector<int>>& graph) {
    auto dist = floyd_warshall(graph);
    int radius = INF;
    for (const auto& row : dist) {
        radius = std::min(radius, *std::max_element(row.begin(), row.end()));
    }
    return radius;
}

std::vector<std::vector<int>> radial_paths(const std::vector<std::vector<int>>& graph,int radius) {
    auto dist = floyd_warshall(graph);
    std::vector<std::vector<int>> paths;
    
    for (int i = 0; i < graph.size(); i++) {
        for (int j = i + 1; j < graph.size(); j++) {
            if (dist[i][j] == radius) {
                std::vector<int> path = {i, j};
                while (true) {
                    int k = -1;
                    for (int l = 0; l < graph.size(); l++) {
                        if (l != path[path.size() - 2] && graph[path[path.size() - 2]][l] != INF && dist[l][j] == dist[path[path.size() - 2]][j] - graph[path[path.size() - 2]][l]) {
                            k = l;
                            break;
                        }
                    }
                    if (k == -1) {
                        break;
                    }
                    path.insert(path.end() - 1, k);
                }
                paths.push_back(path);
            }
        }
    }
    return paths;
}

std::vector<int> centers(std::vector<std::vector<int>> graph) {
    int n = graph.size();
    std::vector<std::vector<int>> dist = floyd_warshall(graph);
    std::vector<int> eccentricities(n);
    for (int i = 0; i < n; ++i) {
        eccentricities[i] = *std::max_element(dist[i].begin(), dist[i].end());
    }
    int min_eccentricity = *std::min_element(eccentricities.begin(), eccentricities.end());
    std::vector<int> centers;
    for (int i = 0; i < n; ++i) {
        if (eccentricities[i] == min_eccentricity) {
            centers.push_back(i + 1);
        }
    }
    return centers;
}

void degree(vector<vector<int>> graph){
    int n = graph.size();
    std::vector<int> degrees(n, 0);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (graph[i][j] != INF) {
                degrees[i]++;
            }
        }
    }
    std::cout << "Степени вершин: ";
    for (int i = 0; i < n; i++) {
        std::cout <<"[ "<<i+1<<" = "<< degrees[i] << " ] ";
    }
    std::cout << std::endl;
}

void dfs(int u, int &time, vector<bool> &visited, vector<int> &discovery,
         vector<int> &low, vector<int> &parent, vector<int> &ap, vector<vector<int>> &graph) {
    int children = 0;
    visited[u] = true;
    discovery[u] = low[u] = time;
    time++;

    for (int v = 0; v < graph.size(); v++) {
        if (graph[u][v] != INF) {
            if (!visited[v]) {
                children++;
                parent[v] = u;
                dfs(v, time, visited, discovery, low, parent, ap, graph);
                low[u] = min(low[u], low[v]);

                if (parent[u] == -1 && children > 1) {
                    ap.push_back(u + 1);
                }
                if (parent[u] != -1 && low[v] >= discovery[u]) {
                    ap.push_back(u + 1);
                }

            } else if (v != parent[u]) {
                low[u] = min(low[u], discovery[v]);
            }
        }
    }
}

vector<int> articulation_points(vector<vector<int>> &graph) {
    int n = graph.size();
    int time = 0;
    vector<bool> visited(n, false);
    vector<int> discovery(n, INF), low(n, INF), parent(n, -1), ap;

    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i, time, visited, discovery, low, parent, ap, graph);
        }
    }

    return ap;
}




// Пример использования
int main() {
    int n = 0;  // количество вершин в графе
    vector<int> vertex = reading_file("data.txt");
    for( auto tow:vertex){
        if(tow > n){
            n = tow;
        }
    }
    vector<vector<int>> g(n, vector<int>(n, INF));
    for(int i=0;i<vertex.size();i+=2){
        int x = vertex[i]-1;
        int y = vertex[i+1]-1;
        g[x][y] = g[y][x] = 1;
    }
    cout<<endl;
    for(auto row:g){
        for(auto col:row){
            if(col == INF){
                cout<< "inf" <<" ";
            }
            else cout<<col<<" ";
        }cout<<endl;
    }

    int diametr = diameter(g);
    cout<<"диаметр графа: "<<diametr<<endl;
    vector<vector<int>> path_diametr = diameter_paths(g,diametr);

    cout<<"диаметральные цепи: "<<endl;
    for(auto row:path_diametr){
        for(auto col:row){
            cout<<col+1<<" ";
        }cout<<endl;
    }cout<<endl;


    int radius = radius_graph(g);
    cout<<"радиус графа: "<<radius<<endl;
    vector<vector<int>> path_radius = radial_paths(g,radius);
    cout<<"радиальные цепи: "<<endl;
    for(auto row:path_radius){
        for(auto col:row){
            cout<<col+1<<" ";
        }cout<<endl;
    }cout<<endl;


    cout<<"центры графа: ";
    vector<int> centres_graph = centers(g);
    for(auto row:centres_graph){
        cout<<row<<" ";
    }cout<<endl;

    degree(g);

    cout<<endl;
    cout<<"точки сочленения: ";
    vector<int> articulation = articulation_points(g);
    for(auto row:articulation){
        cout<<row<<" ";
    }
    


    return 0;
}