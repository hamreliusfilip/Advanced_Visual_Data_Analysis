import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt

# Pre processing the data 
path = 'TNM098-MC3-2011.csv'

df = pd.read_csv(path, delimiter=';')

data = []

for id_value in df['ID']:
    title = df.loc[df['ID'] == id_value, 'Title'].values[0].lower()
    date = df.loc[df['ID'] == id_value, 'Date'].values[0]
    content = df.loc[df['ID'] == id_value, 'Content'].values[0].lower()
    
    tokens = nltk.word_tokenize(content)
    
    stop = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    filtered_tokens = [token for token in tokens if token.lower() not in stop and token.lower() not in punctuation]
    
    filtered_content = ' '.join(filtered_tokens)
    
    data.append([id_value, title, date, filtered_content])

# Subset on relevant key words 
with open('words.txt', 'r') as file:
    keywords = file.read().splitlines()

def filter_content(content):
    tokens = nltk.word_tokenize(content)
    stop = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    filtered_tokens = [token for token in tokens if token.lower() not in stop and token.lower() not in punctuation]
    filtered_content = ' '.join([token for token in filtered_tokens if token.lower() in keywords])
    return filtered_content

filtered_data = [[row[0], row[1], row[2], filter_content(row[3])] for row in data]

for row in filtered_data: 
    id_value, title, date, filtered_content = row
    print(f"Content: {filtered_content}")




# Visualize the temporal data - Density over time
df['Date'] = pd.to_datetime(df['Date'])
dates = df['Date']

min_date = dates.min()
max_date = dates.max()
num_bins = 10  
bin_width = (max_date - min_date) / num_bins
bin_edges = [min_date + i * bin_width for i in range(num_bins + 1)]

plt.hist(dates, bins=bin_edges, density=False)
plt.xlabel('Date')
plt.ylabel('Number of Entries')
plt.title('Distribution of Content Over Time')
plt.show()
