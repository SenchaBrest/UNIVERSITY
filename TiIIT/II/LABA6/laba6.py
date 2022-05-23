import numpy as np
import numpy.random as rand

k = 1
def random_seed():
    global k
    k += 1
    rand.seed(k)
def N(m, scale):
    random_seed()
    r = rand.normal(m, scale, size=None)
    if r < 0: r = 0
    return r
def U(c, d):
    random_seed()
    r = rand.uniform(c, d, size=None)
    if r < 0: r = 0
    return r

amount = 15
workers_distrib = [0.2, 0.3, 0.3, 0.2, 0.0]
def start_workers():
    workers = np.array([[U(0.2, 0.5) * N(6, 0.5) for i in range(int(workers_distrib[0] * amount))],
               [U(0.1, 0.3) * N(5, 0.5) for i in range(int(workers_distrib[1] * amount))],
               [U(0.05, 0.2) * N(4, 0.5) for i in range(int(workers_distrib[2] * amount))],
               [U(0.01, 0.02) * N(2, 0.5) for i in range(int(workers_distrib[3] * amount))],
               [U(0.3, 0.75) * N(1, 0.5) for i in range(int(workers_distrib[4] * amount))]], dtype=object)
    return workers

data = np.empty([0])
for iter in range(100):
    completed_work = 0
    days = 0
    while completed_work < 100:
        workers = start_workers()
        sum = 0
        for i in range(len(workers)):
            for j in range(len(workers[i])):
                sum += workers[i][j]
        completed_work += sum
        days += 1
    data = np.append(data, days)

print("Average number of days: ", np.mean(data))
print("Maximum number of days:", np.amax(data))
print("Minimum number of days:", np.amin(data))