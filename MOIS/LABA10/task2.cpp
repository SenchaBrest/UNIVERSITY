#include <iostream>
#include <limits.h> // Библиотека для работы с числами
#include <queue> // Библиотека для работы с очередью
#include <vector> // Библиотека для работы с векторами
#include <string.h> // Библиотека для работы со строками
using namespace std;
// Функция для поиска пути по алгоритму BFS
bool bfs(vector<vector<int>> rGraph, int s, int t, vector<int>& parent){
    const int V = rGraph.size(); // Получаем количество вершин графа
    bool visited[V]; // Массив для хранения информации о посещенных вершинах
    memset(visited, 0, sizeof(visited)); // Инициализируем массив значением false
    queue<int> q; // Очередь для хранения вершин
    q.push(s); // Добавляем начальную вершину
    visited[s] = true; // Отмечаем начальную вершину как посещенную
    parent[s] = -1; // Родитель начальной вершины устанавливаем как -1 (так как начальная вершина является корнем)
    while (!q.empty()) { // Пока очередь не пуста
        int u = q.front(); // Извлекаем вершину из очереди
        q.pop(); // Удаляем вершину из очереди
        for (int v = 0; v < V; v++) { // Проходим по всем вершинам графа
            if (visited[v] == false && rGraph[u][v] > 0) { // Если вершина не была посещена и между вершинами есть ребро
                if (v == t) { // Если найден путь до конечной вершины
                    parent[v] = u; // Устанавливаем родителя конечной вершины
                    return true; // Возвращаем true, так как путь найден
                }
                q.push(v); // Добавляем вершину в очередь
                parent[v] = u; // Устанавливаем родителя вершины
                visited[v] = true; // Отмечаем вершину как посещенную
            }}}return false; // Если пути до конечной вершины не найдено, то возвращаем false
}

// Функция для реализации алгоритма Форда-Фалкерсона
int fordFulkerson(vector<vector<int>> graph, int s, int t){
    int u, v;
    const int V = graph.size(); // Получаем количество вершин графа
    vector<vector<int>> rGraph(V , vector<int>(V , 0)); // Создаем резидуальный граф
    for (u = 0; u < V ; u++)
        for (v = 0; v < V ; v++)
            rGraph[u][v] = graph[u][v]; // Инициализируем ребра резидуального графа
    vector<int> parent(V); // Создаем массив для хранения родителей каждой вершины в bfs
    int max_flow = 0; // Изначально максимальный поток равен 0
    while (bfs(rGraph, s, t, parent)) { // Пока есть увеличивающий путь в резидуальном графе
        int path_flow = INT_MAX; // Изначально значение потока на пути равно максимальному возможному значению
        for (v = t; v != s; v = parent[v]) { // Находим минимальное значение потока на увеличивающем пути
            u = parent[v];
            path_flow = min(path_flow, rGraph[u][v]);
        }
        for (v = t; v != s; v = parent[v]) { // Обновляем значения ребер на увеличивающем пути и обратных ребер
            u = parent[v];
            rGraph[u][v] -= path_flow;
            rGraph[v][u] += path_flow;
        }max_flow += path_flow; // Добавляем значение потока на увеличивающем пути к общему максимальному потоку
    }cout<<endl;
    for(int i = 0;i<rGraph.size();i++){for(int j = 0;j<rGraph.size();j++){cout<<rGraph[i][j]<<" ";}cout<<endl;}cout<<endl;
    return max_flow; // Возвращаем максимальный поток
}
int main(){
    vector<vector<int>> graph = { 
                    { 0, 7, 8, 0, 0, 0 },
                    { 0, 0, 2, 3, 6, 0 } ,
                    { 0, 0, 0, 2, 2, 0 },
                    { 0, 6, 0, 0, 0, 7 },
                    { 0, 0, 0, 0, 0, 9 },
                    { 0, 0, 0, 0, 0, 0 }};
    cout << "The maximum possible flow is "
         << fordFulkerson(graph, 0, 5); // Вызываем функцию для нахождения максимального потока
    return 0;}
