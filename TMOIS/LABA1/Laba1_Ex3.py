from typing import List

def bitmask(A:List):
    '''Создание битовой маски множества'''
    bitmask = [0 for i in range(len(U))]
    for i in range(len(A)):
        if U.index(A[i]) != -1:
            bitmask[U.index(A[i])] = 1
    return bitmask

def antibitmask(bitmask:List):
    '''Расшифровка битовой маски'''
    set = []
    for i in range(len(bitmask)):
        if bitmask[i] == 1:
            set.append(U[i])
    return set

def union(A:List, B:List):
    '''Объединение'''
    union = [0 for i in range(len(U))]
    a_ = bitmask(A)
    b_ = bitmask(B)
    for i in range(len(a_)):
        union[i] = a_[i] | b_[i]  
    union = antibitmask(union)
    return union

def intersection(A:List, B:List):
    '''Пересечение'''
    intersection = [0 for i in range(len(U))]
    a_ = bitmask(A)
    b_ = bitmask(B)
    for i in range(len(a_)):
        intersection[i] = a_[i] & b_[i]
    intersection = antibitmask(intersection)
    return intersection

def diff(A:List, B:List):
    '''Разность'''
    diff = [0 for i in range(len(U))]
    a_ = bitmask(A)
    b_ = bitmask(B)
    for i in range(len(a_)):
        diff[i] = a_[i] - b_[i]
    diff = antibitmask(diff)
    return diff

def sym_diff(A:List, B:List):
    '''Симметрическая разность'''
    sym_diff = [0 for i in range(len(U))]
    a_ = bitmask(A)
    b_ = bitmask(B)
    for i in range(len(a_)):
        sym_diff[i] = a_[i] ^ b_[i]
    sym_diff = antibitmask(sym_diff)
    return sym_diff
    
def addition(A:List):
    '''"Нe"'''
    a_ = bitmask(A)
    for i in range(len(a_)):
        if a_[i] == 0:
            a_[i] = 1
        else:
            a_[i] = 0
    A = antibitmask(a_)
    return A

U = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
A = [1, 3, 4, 7]
B = [3, 5, 6, 7, 8]
C = [2, 4, 5, 7]

print('\nОбъединение: ')
print(union(A, B))
print('\nПересечение: ')
print(intersection(A, B))
print('\nРазность А и В: ')
print(diff(A, B))
print('\nРазность В и А: ')
print(diff(B, A))
print('\nСимметрическая разность: ')
print(sym_diff(A, B))
print('\nДополнение А: ')
print(addition(A))
print('\nДополнение В: ')
print(addition(B))
print('\nРешение задания 4: ')
print(intersection(A, diff(B, C)))