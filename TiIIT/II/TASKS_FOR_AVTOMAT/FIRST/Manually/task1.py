import numpy as np
import pandas as pd
import numpy.random as rand

alfa = 0.5
c = 0.8745
    
x = pd.read_csv('student-mat.csv', delimiter=',', names=['school', 'sex', 'age', 'address',
                                               'famsize', 'Pstatus', 'Medu', 'Fedu',
                                               'Mjob', 'Fjob', 'reason', 'guardian',
                                               'traveltime', 'studytime', 'failures', 'schoolsup',
                                               'famsup', 'paid', 'activities', 'nursery',
                                               'higher', 'internet', 'romantic', 'famrel',
                                               'freetime', 'goout', 'Dalc', 'Walc',
                                               'health', 'absences', 
                                               
                                               'G1', 'G2', 'G3'])
x['school'] = x['school'].map({"GP": 0, "MS": 1})
x['sex'] = x['sex'].map({"F": 0, "M": 1})
x['address'] = x['address'].map({"U": 0, "R": 1})
x['famsize'] = x['famsize'].map({"LE3": 0, "GT3": 1})
x['Pstatus'] = x['Pstatus'].map({"T": 0, "A": 1})
x['Mjob'] = x['Mjob'].map({"teacher": 0, "health": 1, "services" : 2, "at_home": 3, "other": 4})
x['Fjob'] = x['Fjob'].map({"teacher": 0, "health": 1, "services" : 2, "at_home": 3, "other": 4})
x['reason'] = x['reason'].map({"home": 0, "reputation": 1, "course": 2, "other": 3})
x['guardian'] = x['guardian'].map({"mother": 0, "father": 1, "other": 2})

def y_stroke(m, w):
    global x
    s = w[0]
    for column in range(1, len(x.columns)):
        s += x[x.columns[column - 1]].iloc[m] * w[column]
    return s

def se(y, y_stroke):
    return np.square(np.subtract(y, y_stroke))

w = np.random.normal(0, 0.05, 33)
#w = np.zeros(33)
w_b = np.zeros(33)
for i in range(100):

    for n in range(len(w)):
        w_b[n] = w[n] + alfa * rand.uniform(-1, 1)
    
    sum_se = 0
    for m in range(len(x) - 10):  
        sum_se += se(x['G3'][m], y_stroke(m, w))
    MSE1 = 1 / len(x['G3']) * sum_se

    sum_se = 0
    for m in range(len(x) - 10):  
        sum_se += se(x['G3'][m], y_stroke(m, w_b))
    MSE2 = 1 / len(x['G3']) * sum_se
    
    if MSE2 < MSE1:
        for n in range(len(w)):
            w[n] = w_b[n]
        print("%10f" % (MSE2))
    alfa *= c    

print("\n\n")
print(w)

s = 0
for i in range((len(x) - 10), len(x)):
    a = y_stroke(i, w)
    print(a)
    b = x['G3'][i] - a
    print(b)
    s += np.abs(b)
    print("\n")
print("\n\n")
print(s/10)