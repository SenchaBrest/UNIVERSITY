import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt

def N(m, scale):
    r = rand.normal(m, scale, size=None)
    if r < 0: r = 0
    return r
def U(c, d):
    r = rand.uniform(c-d, c+d, size=None)
    if r < 0: r = 0
    return r
def E(scale):
    r = rand.exponential(scale, size=None)
    if r < 0: r = 0
    return r

class Virus:
    def __init__(self):
        self.I = E(2.5)
corona = Virus()

class Environment:
    def __init__(self):
        self.AP = N(40, 5.5)
        self.M = N(10, 1.5)
        self.T = E(3.5)
region = Environment()

class Agent:
    day = None
    def __init__(self):
        self.m = rand.uniform(0, 50)

        self.is_ill = False
        self.is_know = False
        self.is_on_treatment = False
        self.is_dead = False

        self.SC = int(N(self.m, 5))
        self.R = 1
        self.HA = N(4, 1.5)
        self.A = N(region.AP, 20)

        self.RT = int(2 + N(30 - 2.2 * self.HA, 4 - 0.15 * self.HA))
        self.DR = self.A * 0.11 + U(5 - 0.05 * self.HA - 0.2 * region.M, 2 - 0.1 * self.HA)

    def setRT(self):
        self.RT = int(2 + N(30 - 2.2 * self.HA - 0.8 * region.M,\
             4 - 0.15 * self.HA - 0.12 * region.M))



initial_amount = int(rand.uniform(5, 11))
people = [Agent() for i in range(initial_amount)]
for i in range(initial_amount):
    people[i].is_ill = True
    people[i].day = 0

data = []
k_is_dead = 0
k_is_cured = 0
data.append([0, len(people), k_is_dead, k_is_cured])
print("%3s %8s %6s %6s" % ("DAY", "Infected", "Died", "Cured"))
print("%3d %8d %6d %6d" % (0, len(people), k_is_dead, k_is_cured))
for day in range(30):

    for i in range(len(people)):
        if people[i].is_know == True:
            continue
        probability_T = rand.uniform(0, 100)
        if probability_T < region.T:
            people[i].is_know = True
            people[i].R = U(5, 5)
            people[i].SC /= people[i].R
            people[i].SC = int(people[i].SC)

    for i in range(len(people)):
        probability_HA = rand.uniform(0, 100)
        if people[i].HA < 2:
            if probability_HA < 0.1 * 100:
                people[i].is_on_treatment = True
                people[i].setRT()
        else:
            if probability_HA < 0.01 * 100:
                people[i].is_on_treatment = True
                people[i].setRT()

    index = []
    for i in range(len(people)):
        probability_DR = rand.uniform(0, 100)
        if probability_DR < people[i].DR:
            people[i].is_dead = True
            k_is_dead += 1
            index.append(i)
    for i in index:
        people[i] = None
    for i in index:
        people.remove(None)
        
    index = []
    for i in range(len(people)):
        if people[i].day + people[i].RT == day:
            people[i].is_ill = False
            k_is_cured += 1
            index.append(i)
    for i in index:
        people[i] = None
    for i in index:
        people.remove(None)

    k_new = 0
    for person in people:
        if person.is_on_treatment == True:
            continue
        k_new += person.SC
    people += [Agent() for i in range(k_new)]
    
    index = []
    for i in range(len(people)):
        if people[i].is_ill == True:
            continue
        probability_I = rand.uniform(0, 100)
        if probability_I < corona.I:
            people[i].is_ill = True
            people[i].day = day
        else:
            index.append(i)
    for i in index:
        people[i] = None
    for i in index:
        people.remove(None)

    data.append([day + 1, len(people), k_is_dead, k_is_cured])
    print("%3d %8d %6d %6d" % (day + 1, len(people), k_is_dead, k_is_cured))



data[0].append(0)
data[0].append(0)
data[0].append(0)
for i in range(1, len(data)):
    data[i].append(data[i][1] - data[i - 1][1])
    data[i].append(data[i][2] - data[i - 1][2])
    data[i].append(data[i][3] - data[i - 1][3])
print("\n\n")
print("%3s %9s %6s %6s %9s %6s %6s" % ("DAY", "InfectedG", "DiedG", "CuredG", "Infected+", "Died+", "Cured+"))
for i in range(len(data)):
    print("%3d %8d %6d %6d %9d %6d %6d" % (data[i][0], data[i][1], data[i][2], data[i][3], \
        data[i][4], data[i][5], data[i][6]))
mean = np.mean(data[4])
std = np.std(data[4])
print(f"\n\nMathematical expectation: {int(mean)}; Standard deviation: {int(std)}.")



fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(nrows=3, ncols=3)
ax1 = fig.add_subplot(gs[:-1, :])
ax1.set_title('Infected')
ax2 = fig.add_subplot(gs[-1, :-1])
ax2.set_title('Died')
ax3 = fig.add_subplot(gs[-1, -1])
ax3.set_title('Cured')

day = [i for i in range(len(data))]

infectedG = [data[i][1] for i in range(len(data))]
ax1.bar(day, infectedG, color='red')

diedG = [data[i][2] for i in range(len(data))]
ax2.bar(day, diedG, color='black')

curedG = [data[i][3] for i in range(len(data))]
ax3.bar(day, curedG, color='green')

ax1.grid(), ax2.grid(), ax3.grid()
plt.show()