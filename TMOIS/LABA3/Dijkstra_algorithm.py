import math
import time

def arg_min(T, S):
    amin = -1
    m = math.inf  
    for i, t in enumerate(T):
        if t < m and i not in S:
            m = t
            amin = i
    return amin

if __name__ == '__main__':
    matrix = [[0, 5, 4, 6, 0, 0, 0],
              [5, 0, 0, 3, 0, 0, 0],
              [4, 0, 0, 3, 0, 5, 9],
              [6, 3, 3, 0, 5, 4, 0],
              [0, 0, 0, 5, 0, 0, 3],
              [0, 0, 5, 4, 0, 0, 6],
              [0, 0, 9, 0, 3, 6, 0]]

    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            if column == row: continue
            if matrix[row][column] == 0:
                matrix[row][column] = math.inf

    N = len(matrix)  
    T = [math.inf]*N  

    v = int(input("Enter number of node: ")) - 1 # стартовая вершина (нумерация с нуля)
    S = {v} # просмотренные вершины
    T[v] = 0 # нулевой вес для стартовой вершины
    M = [0]*N # оптимальные связи между вершинами

    start = time.perf_counter()
    while v != -1: # цикл, пока не просмотрим все вершины
        for j, dw in enumerate(matrix[v]): # перебираем все связанные вершины с вершиной v
            if j not in S: # если вершина еще не просмотрена
                w = T[v] + dw
                if w < T[j]:
                    T[j] = w
                    M[j] = v # связываем вершину j с вершиной v
        v = arg_min(T, S) # выбираем следующий узел с наименьшим весом
        if v >= 0: # выбрана очередная вершина
            S.add(v) # добавляем новую вершину в рассмотрение
    end = time.perf_counter()
    print(dict(zip([i for i in range(1, len(matrix) + 1)], T)))
    print(end - start)