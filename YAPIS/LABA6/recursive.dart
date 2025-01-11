void findAllPaths(List<List<int>> graph, int v, int w) {
  List<int> path = [];
  Set<int> visited = {};
  dfs(graph, v, w, visited, path);
}

void dfs(List<List<int>> graph, int v, int w, Set<int> visited, List<int> path) {
  visited.add(v);
  path.add(v);

  if (v == w) {
    print(path);
  } else {
    for (int i = 0; i < graph.length; i++) {
      if (graph[v][i] == 1 && !visited.contains(i)) {
        dfs(graph, i, w, visited, path);
      }
    }
  }

  path.removeLast();
  visited.remove(v);
}

void main(List<String> arguments) {
  List<List<int>> graph = [
    [0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ];

  final int startVertex;
  final int endVertex;
  if (arguments.length == 2) {
    startVertex = int.parse(arguments[0]);
    endVertex = int.parse(arguments[1]);
  } else if (arguments.isEmpty){
    startVertex = 0;
    endVertex = 7;
  } else {
    throw Error();
  }

  print('Все пути от вершины $startVertex до вершины $endVertex:');
  findAllPaths(graph, startVertex, endVertex);
}
