import pickle

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


class CustomBM25:
    def __init__(self, vectorizer, b=0.75, k1=1.6):
        self.vectorizer = vectorizer
        self.b = b
        self.k1 = k1

    def fit(self, X):
        self.vectorizer.fit(X)
        self.y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.avdl = self.y.sum(1).mean()

    def transform(self, q):
        b, k1, avdl = self.b, self.k1, self.avdl
        len_y = self.y.sum(1).A1
        q, = super(TfidfVectorizer, self.vectorizer).transform([q])
        assert sparse.isspmatrix_csr(q)
        # convert to csc for better column slicing
        y = self.y.tocsc()[:, q.indices]
        denom = y + (k1 * (1 - b + b * len_y / avdl))[:, None]
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.
        numer = y.multiply(np.broadcast_to(idf, y.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1


data = pd.read_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/preprocessed_data.pkl')

tfidf_vectorizer = TfidfVectorizer()
bm25 = CustomBM25(tfidf_vectorizer)
bm25.fit(data)
model_file_path = '/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/bm25_model.pkl'

with open(model_file_path, 'wb') as file:
    pickle.dump(bm25, file)

import pickle

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


class CustomBM25:
    def __init__(self, vectorizer, b=0.75, k1=1.6):
        self.vectorizer = vectorizer
        self.b = b
        self.k1 = k1

    def fit(self, X):
        self.vectorizer.fit(X)
        self.y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.avdl = self.y.sum(1).mean()

    def transform(self, q):
        b, k1, avdl = self.b, self.k1, self.avdl
        len_y = self.y.sum(1).A1
        if isinstance(q, list):
            q = ' '.join(q)
        q, = super(TfidfVectorizer, self.vectorizer).transform([q])
        assert sparse.isspmatrix_csr(q)
        # convert to csc for better column slicing
        y = self.y.tocsc()[:, q.indices]
        denom = y + (k1 * (1 - b + b * len_y / avdl))[:, None]
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.
        numer = y.multiply(np.broadcast_to(idf, y.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1


data = pd.read_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/preprocessed_data.pkl')

tfidf_vectorizer = TfidfVectorizer()
bm25 = CustomBM25(tfidf_vectorizer)
bm25.fit(data)
model_file_path = '/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/bm25_model.pkl'

with open(model_file_path, 'wb') as file:
    pickle.dump(bm25, file)
