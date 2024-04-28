import pickle

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_pickle('../assets/preprocessed_data.pkl')


def train_kmeans_model(preprocessed_data, num_clusters=7):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_data)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(tfidf_matrix)
    return kmeans


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(data)
kmeans_model = train_kmeans_model(data)

with open('../assets/kmeans_model.pkl', 'wb') as f:
    pickle.dump(kmeans_model, f)

# Pickle vectorizer
with open('../assets/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)


