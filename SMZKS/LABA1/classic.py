from functools import reduce


def calculate_ctrl_sum(lst, r):
    return list(
        f"{reduce(lambda x, y: x ^ y, (i + 1 for i, x in enumerate(lst) if x == '1')):0{r}b}"
    )


def invert_element(lst, index):
    lst[index] = str(int(lst[index]) ^ 1)
    return lst


M = 200
r = 5

M_binary_str = f"{M:b}"
M_lst = list(M_binary_str)
print(f"M:{M}, r:{r}\n{M_lst}")

while 2 ** r > len(M_lst) + r:
    r -= 1
r += 1

for p in range(r):
    M_lst.insert(2 ** p - 1, '')

print(M_lst)
ctrl_sum1 = calculate_ctrl_sum(M_lst, r)[::-1]
print(ctrl_sum1)
M_lst = [ctrl_sum1.pop(0) if elem == '' and ctrl_sum1 else elem for elem in M_lst]
print(M_lst, end='\n\n')


ctrl_sum2 = calculate_ctrl_sum(M_lst, r)
print(ctrl_sum2)
print(M_lst, end='\n\n')

index = 5
M_lst = invert_element(M_lst, index)
print(M_lst)
control_sum3 = calculate_ctrl_sum(M_lst, r)
print(control_sum3)
error_index = int(''.join(control_sum3), 2) - 1
print(f"error index:{error_index}")
M_lst = invert_element(M_lst, error_index)
print(M_lst)

