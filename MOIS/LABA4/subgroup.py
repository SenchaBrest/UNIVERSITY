mod = 13

def order(n):
    i = 1
    result = n
    while result != 1:
        result = (result * n) % mod
        i += 1
    return i

def cyclic_subgroup(n):
    subgroup = set()
    i = 1
    result = n
    while result not in subgroup:
        subgroup.add(result)
        result = (result * n) % mod
        i += 1
    return subgroup

elements = set(range(1, mod))

for n in elements:
    print("Element:", n)
    print("Order:", order(n))
    print("Sybgroup:", cyclic_subgroup(n))
    print()
