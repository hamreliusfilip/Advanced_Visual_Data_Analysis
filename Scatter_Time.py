import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = 'Data/EyeTrack-raw.tsv'

data=pd.read_csv(path,sep='\t')

X = data['GazePointX(px)']
Y = data['GazePointY(px)']
TIME = data['RecordingTimestamp']

TIME = TIME / 1000

scatter = plt.scatter(X, Y, c=TIME, cmap='viridis')
cbar = plt.colorbar(scatter, label="Time")

plt.xlabel('X - coordinate')
plt.ylabel('Y - coordinate')
plt.title('Eye tracking with color as time')

ticks = np.linspace(min(TIME), max(TIME), num=5)
cbar.set_ticks(ticks)
cbar.set_ticklabels([str(label) for label in ticks])

plt.show()
