import math
from unicodedata import name

def get_min(R, U):
    rm = (math.inf, -1, -1)
    for v in U:
        rr = min(R, key=lambda x: x[0] if (x[1] == v or x[2] == v) and (x[1] not in U or x[2] not in U) else math.inf)
        if rm[0] > rr[0]:
            rm = rr
    return rm

if __name__ == '__main__':
    # список ребер графа (длина, вершина 1, вершина 2)
    # первое значение возвращается, если нет минимальных ребер
    R = [(math.inf, -1, -1), (5, 1, 2), (3, 1, 3), (6, 1, 4), (3, 2, 3), (4, 2, 5),
         (2, 3, 4), (5, 3, 5), (1, 4, 5)]

    N = 6 # число вершин в графе
    U = {1} # множество соединенных вершин
    T = [] # список ребер остова

    while len(U) < N:
        r = get_min(R, U) # ребро с минимальным весом
        if r[0] == math.inf: # если ребер нет, то остов построен
            break
        T.append(r) # добавляем ребро в остов
        U.add(r[1]) # добавляем вершины в множество U
        U.add(r[2])

    print(T)