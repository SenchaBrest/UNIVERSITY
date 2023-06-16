import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
from tqdm import tqdm

COUNT_OF_LAB = 7
SEMESTER_DURATION = 120
# 9:40, 11:20, 12:50, 14:40, 16:10, 17:40, 19:10, 20:40
COUPLES = [9.67, 11.33, 12.83, 14.67, 16.17, 17.67, 19.17, 20.67]

def N(x):
    return 1 / np.sqrt(2 * np.pi * np.square(3)) * \
        np.exp((-1) * np.square(x - 13.5)/ (2 * np.square(3)))
N0 = N(13.5)
def E(x):
    return 1 / 9 * np.exp((-1) * x / 9)
E0 = E(9)

if __name__=="__main__":
    best_couple = []
    surrendered_labs = 0
    for day in tqdm(range(SEMESTER_DURATION)):
        for couple in COUPLES:
            if rand.uniform(0, 1) < N(couple) * E(couple) * (1 / N0) * (1 / E0):
                if rand.uniform(0, 1) < 0.8:
                    surrendered_labs += 1
                    best_couple.append(couple)
            if surrendered_labs == COUNT_OF_LAB:
                print(f'U need {day + 1} days to surrender 7 labs.')
                print(f'U should come in {np.mean(best_couple) - 0.67} of hours.') 
                break
        if surrendered_labs == COUNT_OF_LAB:
            break

# x_plt = np.arange(9, 21, 0.0001)
# f_plt = [E(x) * 1 / E(9) for x in x_plt]

# fig, ax = plt.subplots()
# ax.grid(True)

# ax.plot(x_plt, f_plt)
# plt.show()

fig, ax = plt.subplots()
ax.grid(True)

day = [i for i in range(1, len(best_couple) + 1)]

ax.bar(day, best_couple, color='red')
plt.show()