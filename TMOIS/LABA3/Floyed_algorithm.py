import math
import time

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

    start = time.perf_counter()
    P = [[m for m in range(len(matrix))] for n in range(len(matrix))] 
    for k in range(len(matrix)):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                d = matrix[i][k] + matrix[k][j]
                if matrix[i][j] > d:
                    matrix[i][j] = d
                    P[i][j] = k   
    end = time.perf_counter()
    node = int(input("Enter number of node: "))
    print(dict(zip([i for i in range(1, len(matrix) + 1)], matrix[node - 1])))
    print(end - start)