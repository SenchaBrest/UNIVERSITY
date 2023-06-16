G = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

H = {1, 12}
left_cosets = []

for g in G:
    if g not in H:
        left_coset = set()
        for h in H:
            left_coset.add((g * h) % 13)
        left_cosets.append(left_coset)

print("Factor set G/H:")
for i, coset in enumerate(left_cosets):
    print(f"coset {i+1}: {coset}")
