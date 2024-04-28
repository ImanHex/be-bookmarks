import re
import pandas as pd
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from orderedset import OrderedSet
import pickle

def preProcess(s):
    if not isinstance(s, str):
        return ""

    ps = PorterStemmer()
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    s = [w for w in s if w not in stopwords_set]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    return s

try:
    pickle_file_path = '/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/cleaned_data.pkl'
    cleaned_description = pd.read_pickle(pickle_file_path)
    preProcess_description = cleaned_description.apply(preProcess)

    preProcess_description.to_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/preprocessed_data.pkl')
    # preProcess_description.to_csv('../assets/preprocessed_data.csv',index=False)
    print("preprocess successfully")

except (FileNotFoundError, IOError) as e:
    print(f"Error reading pickle file: {e}")
    raise SystemExit(e)

except Exception as e:
    print(f"Error during processing: {e}")
