def left_cosets(group, subgroup):
    cosets = []
    for g in group:
        coset = set()
        for h in subgroup:
            coset.add((g * h) % len(group))
        cosets.append(coset)
    return cosets

group = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
subgroup = [1]
cosets = left_cosets(group, subgroup)

for i, coset in enumerate(cosets):
    print(f"Left contiguous classes for element {i + 1}: {coset}")
