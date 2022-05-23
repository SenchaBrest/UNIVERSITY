from dataclasses import replace
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
                                               
                                               'G1', 'G2', 'G3'], nrows=380)
x['school'] = x['school'].replace("GP", 0)
x['school'] = x['school'].replace("MS", 1) 

x['sex'] = x['sex'].replace("F", 0)
x['sex'] = x['sex'].replace("M", 1)

x['address'] = x['address'].replace("U", 0)
x['address'] = x['address'].replace("R", 1)

x['famsize'] = x['famsize'].replace("LE3", 0)
x['famsize'] = x['famsize'].replace("GT3", 1)

x['Pstatus'] = x['Pstatus'].replace("T", 0)
x['Pstatus'] = x['Pstatus'].replace("A", 1)

x['Medu'] = x['Medu'].replace("teacher", 1)
x['Medu'] = x['Medu'].replace("health", 1)
x['Medu'] = x['Medu'].replace("teacher", 2)
x['Medu'] = x['Medu'].replace("services", 3)
x['Medu'] = x['Medu'].replace("at_home", 4)
x['Medu'] = x['Medu'].replace("other", 5)

x['Fedu'] = x['Fedu'].replace("teacher", 0)
x['Fedu'] = x['Fedu'].replace("health", 1)
x['Fedu'] = x['Fedu'].replace("teacher", 2)
x['Fedu'] = x['Fedu'].replace("services", 3)
x['Fedu'] = x['Fedu'].replace("at_home", 4)
x['Fedu'] = x['Fedu'].replace("other", 5)

x['Mjob'] = x['Mjob'].replace("teacher", 0)
x['Mjob'] = x['Mjob'].replace("health", 1)
x['Mjob'] = x['Mjob'].replace("teacher", 2)
x['Mjob'] = x['Mjob'].replace("services", 3)
x['Mjob'] = x['Mjob'].replace("at_home", 4)
x['Mjob'] = x['Mjob'].replace("other", 5)

x['Fjob'] = x['Fjob'].replace("teacher", 0)
x['Fjob'] = x['Fjob'].replace("health", 1)
x['Fjob'] = x['Fjob'].replace("teacher", 2)
x['Fjob'] = x['Fjob'].replace("services", 3)
x['Fjob'] = x['Fjob'].replace("at_home", 4)
x['Fjob'] = x['Fjob'].replace("other", 5)

x['reason'] = x['reason'].replace("home", 0)
x['reason'] = x['reason'].replace("reputation", 1)
x['reason'] = x['reason'].replace("course", 2)
x['reason'] = x['reason'].replace("other", 3)

x['guardian'] = x['guardian'].replace("mother", 0)
x['guardian'] = x['guardian'].replace("father", 1)
x['guardian'] = x['guardian'].replace("other", 2)

def y_stroke(m, w):
    global x
    s = w[0]
    for column in range(1, len(x.columns)):
        s += x[x.columns[column - 1]].iloc[m] * w[column]
    return s

def se(y, y_stroke):
    return np.square(np.subtract(y, y_stroke))



#w = np.random.normal(0, 0.05, 33)
w = np.zeros(33)
w_b = np.zeros(33)
for i in range(100):

    for n in range(len(w)):
        w_b[n] = w[n] + alfa * rand.uniform(-1, 1)
    
    sum_se = 0
    for m in range(len(x)):  
        sum_se += se(x['G3'][m], y_stroke(m, w))
    MSE1 = 1 / len(x['G3']) * sum_se

    sum_se = 0
    for m in range(len(x)):  
        sum_se += se(x['G3'][m], y_stroke(m, w_b))
    MSE2 = 1 / len(x['G3']) * sum_se
    
    if MSE2 < MSE1:
        for n in range(len(w)):
            w[n] = w_b[n]
        print("%10f" % (MSE2))
    alfa *= c
    

print("\n\n")

print(w)

x = pd.read_csv('ex.csv', delimiter=',', names=['school', 'sex', 'age', 'address',
                                               'famsize', 'Pstatus', 'Medu', 'Fedu',
                                               'Mjob', 'Fjob', 'reason', 'guardian',
                                               'traveltime', 'studytime', 'failures', 'schoolsup',
                                               'famsup', 'paid', 'activities', 'nursery',
                                               'higher', 'internet', 'romantic', 'famrel',
                                               'freetime', 'goout', 'Dalc', 'Walc',
                                               'health', 'absences', 
                                               
                                               'G1', 'G2', 'G3'])
x['school'] = x['school'].replace("GP", 0)
x['school'] = x['school'].replace("MS", 1) 

x['sex'] = x['sex'].replace("F", 0)
x['sex'] = x['sex'].replace("M", 1)

x['address'] = x['address'].replace("U", 0)
x['address'] = x['address'].replace("R", 1)

x['famsize'] = x['famsize'].replace("LE3", 0)
x['famsize'] = x['famsize'].replace("GT3", 1)

x['Pstatus'] = x['Pstatus'].replace("T", 0)
x['Pstatus'] = x['Pstatus'].replace("A", 1)

x['Medu'] = x['Medu'].replace("teacher", 1)
x['Medu'] = x['Medu'].replace("health", 1)
x['Medu'] = x['Medu'].replace("teacher", 2)
x['Medu'] = x['Medu'].replace("services", 3)
x['Medu'] = x['Medu'].replace("at_home", 4)
x['Medu'] = x['Medu'].replace("other", 5)

x['Fedu'] = x['Fedu'].replace("teacher", 0)
x['Fedu'] = x['Fedu'].replace("health", 1)
x['Fedu'] = x['Fedu'].replace("teacher", 2)
x['Fedu'] = x['Fedu'].replace("services", 3)
x['Fedu'] = x['Fedu'].replace("at_home", 4)
x['Fedu'] = x['Fedu'].replace("other", 5)

x['Mjob'] = x['Mjob'].replace("teacher", 0)
x['Mjob'] = x['Mjob'].replace("health", 1)
x['Mjob'] = x['Mjob'].replace("teacher", 2)
x['Mjob'] = x['Mjob'].replace("services", 3)
x['Mjob'] = x['Mjob'].replace("at_home", 4)
x['Mjob'] = x['Mjob'].replace("other", 5)

x['Fjob'] = x['Fjob'].replace("teacher", 0)
x['Fjob'] = x['Fjob'].replace("health", 1)
x['Fjob'] = x['Fjob'].replace("teacher", 2)
x['Fjob'] = x['Fjob'].replace("services", 3)
x['Fjob'] = x['Fjob'].replace("at_home", 4)
x['Fjob'] = x['Fjob'].replace("other", 5)

x['reason'] = x['reason'].replace("home", 0)
x['reason'] = x['reason'].replace("reputation", 1)
x['reason'] = x['reason'].replace("course", 2)
x['reason'] = x['reason'].replace("other", 3)

x['guardian'] = x['guardian'].replace("mother", 0)
x['guardian'] = x['guardian'].replace("father", 1)
x['guardian'] = x['guardian'].replace("other", 2)

s = 0
for i in range(len(x)):
    a = y_stroke(i, w)
    print(a)
    b = x['G3'][i] - a
    print(b)
    s += np.abs(b)
    print("\n")
print("\n\n")
print(s/len(x))


