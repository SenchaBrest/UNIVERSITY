import time
start_time = time.time()

def lex(count, pos, p, used):
    if pos == count:
        for i in range(count):
            print(str[p[i]], end='')
        print('')
    for i in range(count):
        if not used[i]:
            used[i] = True
            p[pos] = i

            lex(count, pos + 1, p, used)

            p[pos] = 0
            used[i] = False

def antylex(count, pos, p, used):
    if pos == -1:
        for i in range(count - 1, -1, -1):
            print(str[p[i]], end='')
        print('')
    for i in range(count - 1, -1, -1):
        if not used[i]:
            used[i] = True
            p[pos] = i

            antylex(count, pos - 1, p, used)

            p[pos] = 0
            used[i] = False

str = input()
count = len(str)

p = [0 for i in range(count)]
used = [False for i in range(count)]

print("Lexicographic permutation:")
lex(count, 0, p, used)
print("Antilexicographic permutation:")
antylex(count, count-1, p, used)

print("--- %s seconds ---" % (time.time() - start_time))