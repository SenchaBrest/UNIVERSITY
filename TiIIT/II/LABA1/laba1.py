import random
import math

print('Enter extreme numbers along the ordinate:')
y1 = float(input())
y2 = float(input())
print('Enter extreme numbers along the abscissa:')
x1 = float(input())
x2 = float(input())

def func(x):
    y = math.log(x) / x
    return y

def examination(y1, y2, x1, x2, N): 
    n = i = 0
    while i <= N:
        y_random = random.uniform(y1, y2)
        x_random = random.uniform(x1, x2)

        f = func(x_random)
        if f >= 0:
            if y_random <= f:
                if y_random >= 0:
                    n += 1#true
                else:
                    pass#false
            else:
                pass#false
        else:
            if y_random < f:
                pass#false
            else:
                if y_random > 0:
                    pass#false
                else:
                    n += 1#true
        
        i += 1
    return n

def Print(N):
    n = examination(y1, y2, x1, x2, N)
    P = n/N
    S = (y2-y1)*(x2-x1)*P
    error = abs(S-0.240226507)/0.240226507
    print(f'\nThe integral with N equal {N} is {S}, n = {n} and Error is {error}\n')

Print(100)
Print(500)
Print(1000)
Print(3000)
Print(10000)

    