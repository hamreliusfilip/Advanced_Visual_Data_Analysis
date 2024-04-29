import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt

path = 'TNM098-MC3-2011.csv'

df = pd.read_csv(path, delimiter=';')

data = []

for id_value in df['ID']:
    title = df.loc[df['ID'] == id_value, 'Title'].values[0].lower()
    date = pd.to_datetime(df.loc[df['ID'] == id_value, 'Date'].values[0]) 
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
    
topic_assignments = lda_model.transform(tfidf_matrix)
df['Topic'] = topic_assignments.argmax(axis=1)

topic_distribution = df['Topic'].value_counts()
print("Distribution of documents across topics:")
print(topic_distribution)
