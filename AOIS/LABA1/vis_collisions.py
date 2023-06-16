import matplotlib.pyplot as plt
from collisions import data

x = [data[i][0] for i in range(len(data))]
y = [data[i][1] for i in range(len(data))]

plt.plot(x, y)
plt.xlabel('rows')
plt.ylabel('collisions')
plt.title("Collisios for each row")
plt.show()