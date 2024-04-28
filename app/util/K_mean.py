import pandas as pd
from nltk import PorterStemmer, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

def preProcess(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    stopwords_set = set(stopwords.words())
    s = [w for w in s if w not in stopwords_set]
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    return s


def suggest_recipes(user_query, kmeans_model, vectorizer, data, num_recommendations=12):
    # Preprocess user query
    preprocessed_query = preProcess(user_query)
    query_vector = vectorizer.transform([preprocessed_query])

    # Predict the cluster label for the user query
    cluster_label = kmeans_model.predict(query_vector)[0]

    # Filter data to include only recipes belonging to the predicted cluster
    cluster_indices = (kmeans_model.labels_ == cluster_label)
    cluster_recipes = data[cluster_indices]

    # Sample a subset of recipes from the cluster, limited by num_recommendations
    sampled_recipes = cluster_recipes.sample(min(num_recommendations, len(cluster_recipes)))

    # Convert sampled_recipes to a DataFrame if it's not already one
    if not isinstance(sampled_recipes, pd.DataFrame):
        sampled_recipes = sampled_recipes.to_frame()

    # Create a dictionary of recipe indices and their descriptions
    recommendations = {}
    for index, row in sampled_recipes.iterrows():
        recommendations[index] = row['Merged']  # Replace 'Description' with the actual column name

    return recommendations





# cluster_recipesuser_query = "cake"
# recommendations = suggest_recipes(user_query, kmeans_model, vectorizer, data)
# print("Recommended Recipes:")
# print(recommendations)
