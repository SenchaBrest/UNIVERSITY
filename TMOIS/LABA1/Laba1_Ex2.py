from typing import List

def merge_two_list(a:List, b:List):
    # инициализируем список для слияния
    c = []
    i = j = 0
    # сравниваем значение элемента с одного списка 
    # со значением элемента с другого списка
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    # если списки были неодинаковой длины, 
    # попадаем в одно из следующих условий
    if i < len(a):
        c += a[i:]
    if j < len(b):
        c += b[j:]
    return c

def merge_sort(list):
    if len(list) == 1:
        return list
    # находим середину
    middle = len(list) // 2
    # делим список
    left = merge_sort(list[:middle])
    right = merge_sort(list[middle:])
    # сливаем списки и возвращаем их
    return merge_two_list(left, right)

# вводим список
list = [int(i) for i in input('Введите список: ').split(' ')]
# выводим список
print(merge_sort(list))