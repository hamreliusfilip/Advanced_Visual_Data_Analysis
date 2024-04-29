import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis.sklearn
import matplotlib.pyplot as plt
import numpy as np

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

contents = [row[3] for row in data]

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(contents)

num_topics = 5

lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)

lda_model.fit(tfidf_matrix)

feature_names = tfidf_vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda_model.components_):
    print(f"Topic {topic_idx + 1}:")
    top_features_ind = topic.argsort()[:-6:-1]
    top_features = [feature_names[i] for i in top_features_ind]
    print(", ".join(top_features))


document_topic_distribution = lda_model.transform(tfidf_matrix)

for i, topic_dist in enumerate(document_topic_distribution):
    print(f"Document {i + 1}:")
    for topic_idx, prob in enumerate(topic_dist):
        print(f"Topic {topic_idx + 1}: {prob:.4f}")
        
        
from collections import defaultdict
from datetime import datetime

# Create a dictionary to store documents by topic
documents_by_topic = defaultdict(list)

# Iterate through documents and assign them to topics
for i, topic_dist in enumerate(document_topic_distribution):
    dominant_topic = topic_dist.argmax()  # Get the dominant topic for the document
    documents_by_topic[dominant_topic].append((i, df['Date'][i]))

# Analyze temporal distribution for each topic
for topic_idx, documents in documents_by_topic.items():
    print(f"Topic {topic_idx + 1}:")
    document_dates = [datetime.strptime(date, "%Y-%m-%d") for _, date in documents]
    document_dates.sort()  # Sort dates in chronological order
    if document_dates:
        print(f"Earliest report: {document_dates[0].strftime('%Y-%m-%d')}")
        print(f"Latest report: {document_dates[-1].strftime('%Y-%m-%d')}")
        print(f"Number of reports: {len(document_dates)}")
        print()
    else:
        print("No reports for this topic.")



