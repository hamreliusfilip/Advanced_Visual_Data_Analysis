import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = 'Data/EyeTrack-raw.tsv'

data=pd.read_csv(path,sep='\t')

X = data['GazePointX(px)']
Y = data['GazePointY(px)']

scatter = plt.scatter(X, Y)

plt.xlabel('X - coordinate')
plt.ylabel('Y - coordinate')

plt.show()
