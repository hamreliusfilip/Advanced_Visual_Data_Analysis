import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import cm
import pandas as pd
from celluloid import Camera

path = 'Data/EyeTrack-raw.tsv'

data = pd.read_csv(path, sep='\t')

X = data['GazePointX(px)']
Y = data['GazePointY(px)']
TIME = data['RecordingTimestamp'] / 1000

cmap = cm.get_cmap('viridis')
norm = plt.Normalize(TIME.min(), TIME.max())

fig, ax = plt.subplots()
camera = Camera(fig)

for i in range(len(X)):
    plt.scatter(X[i], Y[i], color=cmap(norm(TIME[i])), s=300)
    camera.snap()

animation = camera.animate(interval=100, blit=True)

plt.show()
