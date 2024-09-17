def invert_element(lst, index):
    """Инвертирует элемент списка по указанному индексу (0 -> 1, 1 -> 0)."""
    lst[index] = str(int(lst[index]) ^ 1)
    return lst


# Исходные данные
M = 202  # Число для кодирования
r = 4  # Начальное значение для вычисления количества проверочных бит

# Преобразуем число M в двоичную строку длиной до 7 бит
M_binary_str = f"{M:b}"[:7]
M_lst = list(M_binary_str)
print("M в двоичной системе       :", M_lst)

# Определение минимального количества проверочных бит
while 2 ** r > len(M_lst) + r:
    r -= 1
r += 1

# Добавляем проверочные биты на позиции 2^p - 1
for p in range(r):
    M_lst.insert(2 ** p - 1, '0')

print("M с проверочными битами    :", M_lst)

# Рассчитываем позиции для проверки (перекрытие битов для каждого проверочного бита)
C_overlaps = [
    [
        j for i in range(2 ** k, len(M_lst) + 1, 2 ** (k + 1))
        for j in range(i, i + 2 ** k) if j < len(M_lst) + 1
    ]
    for k in range(r)
]
print("Перекрывающиеся позиции    :", C_overlaps)

# Вычисляем значения проверочных битов
C = [
    sum([int(M_lst[i - 1]) for i in C_overlaps[j]]) % 2
    for j in range(r)
]
print("Значения проверочных битов :", C)

# Записываем проверочные биты на соответствующие позиции
for p in range(r):
    M_lst[2 ** p - 1] = str(C[p])

print("M после установки битов    :", M_lst)

# Инвертируем один бит для моделирования ошибки
M_lst = invert_element(M_lst, 5)
M_lst = invert_element(M_lst, 3)

print("M после инверсии (ошибка)  :", M_lst)

# Проверка кодов Хемминга
CC = [
    str(sum([int(M_lst[i - 1]) for i in C_overlaps[j]]) % 2)
    for j in range(r)
]
print("Пересчитанные проверочные  :", CC)

# Определение индекса ошибки
error_index = int(''.join(CC), 2) - 1
print("Найденный индекс ошибки    :", error_index)

# Исправляем ошибку
M_lst = invert_element(M_lst, error_index)
print("M после исправления ошибки :", M_lst)

# Пересчитываем проверочные биты после исправления
CC = [
    str(sum([int(M_lst[i - 1]) for i in C_overlaps[j]]) % 2)
    for j in range(r)
]

error_index = int(''.join(CC), 2) - 1
print("Индекс ошибки после проверки:", error_index, "Проверочные биты:", CC)

# # Исправляем ошибку
# M_lst = invert_element(M_lst, error_index)
# print("M после исправления ошибки :", M_lst)
#
# # Пересчитываем проверочные биты после исправления
# CC = [
#     str(sum([int(M_lst[i - 1]) for i in C_overlaps[j]]) % 2)
#     for j in range(r)
# ]
#
# error_index = int(''.join(CC), 2) - 1
# print("Индекс ошибки после проверки:", error_index, "Проверочные биты:", CC)
