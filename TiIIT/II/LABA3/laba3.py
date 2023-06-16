import numpy as np
import matplotlib.pyplot as plt

def f(x):
    b = 10
    a = 9
    return np.cos(x) + (1 / b) * np.cos(a * x + 1) \
        + (1 / b ** 2) * np.cos(a ** 2 * x + 2) \
        + (1 / b ** 3) * np.cos(a ** 3 * x + 3) \
        + (1 / b ** 4) * np.cos(a ** 4 * x + 4)

x_plt = np.arange(-10, 10, 0.0001)
f_plt = [f(x) for x in x_plt]

fig, ax = plt.subplots()
ax.grid(True)

ax.plot(x_plt, f_plt)
point = ax.scatter(9.32553, -1.10529, color = 'red')

plt.show()

