import collections

def bfs(graph, root): 
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    while queue: 
        vertex = queue.popleft()
        for neighbour in graph[vertex]: 
            if neighbour not in visited: 
                visited.add(neighbour) 
                queue.append(neighbour) 
    return visited

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in set(graph[start]) - visited:
        dfs(graph, next, visited)
    return visited

if __name__ == '__main__':
    graph = {0: [1, 2, 3], 
             1: [0, 2, 3], 
             2: [0, 1, 3, 4], 
             3: [0, 1, 2, 4, 5],
             4: [2, 3, 5],
             5: [3, 4]} 

    visited = bfs(graph, 0)
    count = 1
    for node in graph:
        if node not in visited:
            visited = bfs(graph, node)
            count += 1
    print(f'BFS: count = {count}')

    visited = dfs(graph, 0)
    count = 1
    for node in graph:
        if node not in visited:
            visited = dfs(graph, node)
            count += 1
    print(f'DFS: count = {count}')     