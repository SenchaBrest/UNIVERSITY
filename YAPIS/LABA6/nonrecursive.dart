void findAllPathsNonRecursive(List<List<int>> graph, int v, int w) {
  List<List<int>> stack = [];
  stack.add([v]);

  while (stack.isNotEmpty) {
    List<int> path = stack.removeLast();
    int current = path.last;

    if (current == w) {
      print(path);
    } else {
      for (int i = 0; i < graph.length; i++) {
        if (graph[current][i] == 1 && !path.contains(i)) {
          List<int> newPath = List.from(path);
          newPath.add(i);
          stack.add(newPath);
        }
      }
    }
  }
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
  } else if (arguments.isEmpty) {
    startVertex = 0;
    endVertex = 7;
  } else {
    throw Error();
  }

  print('Все пути от вершины $startVertex до вершины $endVertex:');
  findAllPathsNonRecursive(graph, startVertex, endVertex);
}
