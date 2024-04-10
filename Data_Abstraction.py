# Import any necessary libraries here
import pandas as pd

path = 'Advanced_Visual_Data_Analysis\Data\EyeTrack-raw.tsv'

data=pd.read_csv(path,sep='\t')

x_vals = data['GazePointX(px)']
y_vals = data['GazePointY(px)']
timestamps = data['RecordingTimestamp']

print(timestamps)

# Write your main code logic here

# If needed, you can call your functions or instantiate your classes here
