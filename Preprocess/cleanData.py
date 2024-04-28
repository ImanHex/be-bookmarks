import pandas as pd
import string
import pickle


def get_and_clean_data(data):
    description = data.drop(
        columns=['PrepTime', 'Description','Unnamed: 0','Images'])

    print("Uses Column", description.columns)

    description.fillna('No Data Provided', inplace=True)

    description['RecipeInstructions'] = description['RecipeInstructions'].apply(lambda s: s.lstrip('c'))
    description['RecipeIngredientParts'] = description['RecipeIngredientParts'].apply(lambda s: s.lstrip('c'))

    # New step: Merge all columns into one
    description['Merged'] = description.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    description['Merged'].fillna('No Data Provided', inplace=True)

    description['Merged'] = description['Merged'].apply(
        lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')).lower()
        .translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), '')))

    description['Merged'] = description['Merged'].drop_duplicates().copy()  # remove duplicate row
    print("cleaned data success")

    # cleaned_description['Merged'] = cleaned_description.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    print(description['Merged'])

    try:
        # Select only the 'Merged' column to save
        merged_data = description['Merged']
        pickle.dump(merged_data, open('../assets/cleaned_data.pkl', 'wb'))
    except Exception as e:
        print(f"Error saving merged data: {e}")
        return None

    return merged_data


try:
    data = pd.read_csv('../assets/final_recipes.csv')
    new_df = get_and_clean_data(data)
    if new_df is not None:
        print("Data cleaning and successful.")
    else:
        print("Data cleaning failed.")
except Exception as e:
    print(f"Error loading data: {e}")
