import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import sys

path = 'Advanced_Visual_Data_Analysis\Data\EyeTrack-raw.tsv'

data=pd.read_csv(path,sep='\t')

X = data['GazePointX(px)']
Y = data['GazePointY(px)']
TIME = data['RecordingTimestamp']

TIME = TIME / 1000

fig, ax = plt.subplots()
scatter = plt.scatter(X, Y, c=TIME, cmap='viridis')
cbar = plt.colorbar(scatter, label="Time")

plt.xlabel('X - coordinate')
plt.ylabel('Y - coordinate')
plt.title('Eye tracking with color as time')

ticks = np.linspace(min(TIME), max(TIME), num=5)
cbar.set_ticks(ticks)
cbar.set_ticklabels([str(label) for label in ticks])


def update(frame):
    # for each frame, update the data stored on each artist.
    x = ticks[:frame]
    y = ticks[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scatter.set_offsets(data)
    return (scatter)


ani = animation.FuncAnimation(fig = fig, func=update, frames=40, interval=30)
plt.show()
