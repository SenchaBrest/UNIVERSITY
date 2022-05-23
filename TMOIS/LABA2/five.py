permutations = []
def lex(count, pos, p, used):
    global permutations 
    if pos == count:
        s = ''
        for i in range(count):
            s += str[p[i]]
        permutations.append(s)
    for i in range(count):
        if not used[i]:
            used[i] = True
            p[pos] = i

            lex(count, pos + 1, p, used)

            p[pos] = 0
            used[i] = False

print("Enter the string: ")
str = input()
count = len(str)

p = [0 for i in range(count)]
used = [False for i in range(count)]

lex(count, 0, p, used)

print("Enter the subset power: ")
k = int(input())

for i in range(len(permutations)):
    permutations[i] = permutations[i][:k]

permutations_k = []
for item in permutations: 
    if item not in permutations_k: 
        permutations_k.append(item)
print(*permutations_k)

