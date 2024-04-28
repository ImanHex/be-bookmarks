import re
from nltk import PorterStemmer
from spellchecker import SpellChecker


def preprocess_query(query):
    query = query.lower()
    words = re.findall(r'\b\w+\b', query)

    spell = SpellChecker()
    misspelled = spell.unknown(words)

    corrected_words = []
    suggestions = {}
    for word in words:
        if word in misspelled:
            corrected_word = spell.correction(word)
            suggestions[word] = corrected_word
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)

    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in corrected_words]

    # Join corrected and stemmed words
    corrected_query = " ".join(corrected_words)
    stemmed_query = " ".join(stemmed_words)

    return corrected_query, stemmed_query, suggestions

