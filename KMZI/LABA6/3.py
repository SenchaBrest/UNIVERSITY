ar = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
]


def get_sum(bitset: list):
    bitset = [0, 0] + [bitset[0]] + [0] + bitset[1:4] + [0] + bitset[4:]
    return [sum([ar[i][j] & bitset[j] for j in range(15)]) % 2 for i in range(4)]


def check_sum(bitset, s):
    bitset = [s[0], s[1]] + [bitset[0]] + [s[2]] + bitset[1:4] + [s[3]] + bitset[4:]
    pb = sum(bitset) % 2
    r = [sum([ar[i][j] & bitset[j] for j in range(15)]) % 2 for i in range(4)]

    if all(r): return "Сумма верная!", f"{pb=}"
    return int("".join([str(int(s)) for s in r[::-1]]), 2), r, f"{pb=}"

str1 = "11000000110"
bitset = [int(x) for x in str1]  # input("Введите последовательность: "`)
s = get_sum(bitset)
print(s)
# bitset[6] = not bitset[6]
# bitset[3] = not bitset[3]

print(check_sum(bitset, s))