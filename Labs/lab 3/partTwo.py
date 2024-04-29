import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import matplotlib.pyplot as plt

# Preprocessing the data
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

# Subset on relevant keywords
with open('words.txt', 'r') as file:
    keywords = file.read().splitlines()


def filter_data(data):
    filtered_data = []
    for row in data:
        id_value, title, date, content = row
        tokens = nltk.word_tokenize(content)
        stop = set(stopwords.words('english'))
        punctuation = set(string.punctuation)
        filtered_tokens = [token for token in tokens if token.lower() not in stop and token.lower() not in punctuation]
        filtered_keywords = [token for token in filtered_tokens if token.lower() in keywords]
        if filtered_keywords:
            filtered_content = ' '.join(filtered_keywords)
            filtered_data.append([id_value, title, date, filtered_content])
    return filtered_data

filtered_data = filter_data(data)

for row in filtered_data:
    id_value, title, date, content = row
    print(f"Content: {content}")


# Count occurrences of each date in original and filtered data
original_date_counts = df['Date'].value_counts().sort_index()
filtered_date_counts = pd.DataFrame(filtered_data)[2].value_counts().sort_index()

# Plotting
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Original data plot
axes[0].bar(original_date_counts.index, original_date_counts.values, color='blue', alpha=0.5, label='Original Data')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Number of Entries')
axes[0].set_title('Distribution of Content Over Time (Original Data)')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=45)

# Filtered data plot
axes[1].bar(filtered_date_counts.index, filtered_date_counts.values, color='red', alpha=0.5, label='Filtered Data')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Number of Entries')
axes[1].set_title('Distribution of Filtered Content Over Time')
axes[1].legend()
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
