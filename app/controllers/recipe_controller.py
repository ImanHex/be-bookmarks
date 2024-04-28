from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd

from app import db
from app.models import UserQuery
from app.util.spellChecker import preprocess_query
from Preprocess.BM25 import CustomBM25
from app.util.K_mean import suggest_recipes

recipe_blueprint = Blueprint('recipe', __name__)

bm25_model_path = '/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/bm25_model.pkl'
recipes_data_path = '/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/final_recipes.csv'
kmeans_model = pd.read_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/kmeans_model.pkl')
vectorizer = pd.read_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/vectorizer.pkl')
data = pd.read_pickle('/Users/mahsoomsateemae/Desktop/Backend-bookmarks/assets/preprocessed_data.pkl')

def get_recipe_details_by_index(index):
    df = pd.read_csv(recipes_data_path)
    if index in df.index:
        row_data = df.loc[df.index == index].iloc[0]
        return {
            'index': int(index),
            'name': row_data.get('Name', 'Name not found'),
            'images': row_data.get('Images', 'No Data Provide'),
            'prep_time': row_data.get('PrepTime', 'No Data Provide'),
            'description': row_data.get('Description', 'No Description'),
            'recipe_instructions': row_data.get('RecipeInstructions', 'No Instructions'),
        }
    return None


@recipe_blueprint.route('/search', methods=['POST'])
def recipe_search_with_name():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    user_query = request.json.get('query', '')
    bm25 = pd.read_pickle(bm25_model_path)

    corrected_query, stemmed_query, suggestions = preprocess_query(user_query)

    scores = bm25.transform(stemmed_query)
    top_10_indices = np.argsort(-scores)[:12]

    top_indices = [idx for idx in top_10_indices if scores[idx] > 0]

    # If no top indices found, return suggestions
    if not top_indices:
        return jsonify({
            'message': 'No recipes found matching your query with a score above 0.',
            'suggestions': suggestions
        }), 200

    # Get results for top indices
    results = [get_recipe_details_by_index(idx) for idx in top_indices if get_recipe_details_by_index(idx)]

    # Save the user query to the database
    user_query_obj = UserQuery(query_text=user_query)
    db.session.add(user_query_obj)
    db.session.commit()

    # Update past query embeddings and suggested recipes
    # latest_query_embedding = convert_query_to_embedding(user_query, load_vectorizer(bm25_model_path))
    # recommended_recipe_indices = [result['index'] for result in results]
    # recommender.update_data(latest_query_embedding, recommended_recipe_indices)

    return jsonify({'query': corrected_query, 'results': results}), 200



@recipe_blueprint.route('/recipe/<int:index>', methods=['GET'])
def search_index(index):
    recipe_details = get_recipe_details_by_index(index)
    if recipe_details:
        return jsonify(recipe_details), 200
    else:
        return jsonify({'message': 'Recipe not found.'}), 404


@recipe_blueprint.route('/recommend', methods=['GET'])
def recommend_recipes():
    latest_query = UserQuery.query.order_by(UserQuery.timestamp.desc()).first()
    if latest_query:
        user_query = latest_query.query_text
        recommendations = suggest_recipes(user_query, kmeans_model, vectorizer, data)
        results = []
        for index, description in recommendations.items():
            recipe_details = get_recipe_details_by_index(int(index))
            if recipe_details:
                recipe_details['description'] = description
                results.append(recipe_details)
        return jsonify({'query': user_query, 'results': results})
    else:
        return jsonify({'message': 'No user queries found.'}), 404






