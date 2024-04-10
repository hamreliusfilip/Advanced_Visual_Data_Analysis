import matplotlib.pyplot as plt
import numpy as np

X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
TIME = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

scatter = plt.scatter(X, Y, c=TIME, cmap='viridis')
cbar = plt.colorbar(scatter, label="Time")

plt.xlabel('X - coordinate')
plt.ylabel('Y - coordinate')
plt.title('Eye tracking with color as time')

ticks = np.linspace(min(TIME), max(TIME), num=5)
cbar.set_ticks(ticks)
cbar.set_ticklabels([str(label) for label in ticks])

plt.show()
