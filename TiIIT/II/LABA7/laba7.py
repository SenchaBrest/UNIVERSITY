import numpy as np
import pandas as pd
import numpy.random as rand

alfa = 1
c = 0.8745

def y_stroke(x1, x2, x3,w0,  w1, w2, w3):
    return w0 + x1 * w1 + x2 * w2 + x3 * w3
def se(y, y_stroke):
    return np.square(np.subtract(y, y_stroke))
    
x = pd.read_csv('x.csv', delimiter=' ', names=['1', '2', '3'])
x1 = x['1']
x2 = x['2']
x3 = x['3']
y = pd.read_csv('y.csv', names=['y'])


w0 = rand.uniform(0, 100)
w1 = rand.uniform(0, 100)
w2 = rand.uniform(0, 100)
w3 = rand.uniform(0, 100)

for i in range(100):

    w00 = w0 + alfa * rand.uniform(-1, 1)
    w11 = w1 + alfa * rand.uniform(-1, 1)
    w22 = w2 + alfa * rand.uniform(-1, 1)
    w33 = w3 + alfa * rand.uniform(-1, 1)

    sum_se = 0
    for i in range(len(x)):  
        sum_se += se(y['y'][i], y_stroke(x1[i], x2[i], x3[i], w0, w1, w2, w3))
    MSE1 = 1 / len(y) * sum_se

    sum_se = 0
    for i in range(len(x)):  
        sum_se += se(y['y'][i], y_stroke(x1[i], x2[i], x3[i], w00, w11, w22, w33))
    MSE2 = 1 / len(y) * sum_se
    
    if MSE2 < MSE1:
        w0 = w00
        w1 = w11
        w2 = w22        
        w3 = w33
        print("%10f" % (MSE2))
    alfa *= c
    

print("\n\n")
print("%10f %10f %10f %10f" % (w0, w1, w2, w3))