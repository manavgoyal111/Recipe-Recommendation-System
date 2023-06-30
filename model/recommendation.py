import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from parse import ingredient_parser
import pickle
import unidecode
import ast


def get_recommendations(N, scores):
    # load in recipe dataset
    df_recipes = pd.read_csv("data/Parsed_Recipe.csv")
    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(
        columns=['recipe', 'ingredients', 'score', 'url'])
    count = 0
    for i in top:
        recommendation.at[count, 'recipe'] = title_parser(
            df_recipes['Title'][i])
        recommendation.at[count, 'ingredients'] = ingredient_parser_final(
            df_recipes['Parsed_Ingredients'][i])
        recommendation.at[count, 'url'] = df_recipes['URL'][i]
        recommendation.at[count, 'ctime'] = df_recipes['Cooking Time'][i]
        recommendation.at[count, 'directions'] = df_recipes['Directions'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        count += 1
    return recommendation


def title_parser(title):
    title = unidecode.unidecode(title)
    return title


# neaten the ingredients being outputted
def ingredient_parser_final(ingredient):
    ingredients = ingredient
    # if isinstance(ingredient, list):
    # else:
    #     ingredients = ast.literal_eval(ingredient)

    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients


def RecSys(ingredients, N=5):
    """
    The reccomendation system takes in a list of ingredients and returns a list of top 5 
    recipes based of of cosine similarity. 
    :param ingredients: a list of ingredients
    :param N: the number of reccomendations returned 
    :return: top 5 reccomendations for cooking recipes
    """

    # load in tdidf model and encodings
    with open("data/encoding.pkl", 'rb') as f:
        tfidf_encodings = pickle.load(f)
    with open("data/model.pkl", "rb") as f:
        tfidf = pickle.load(f)

    # parse the ingredients using my ingredient_parser
    try:
        ingredients_parsed = ingredient_parser(ingredients)
    except:
        ingredients_parsed = ingredient_parser([ingredients])

    # use our pretrained tfidf model to encode our input ingredients
    ingredients_tfidf = tfidf.transform([ingredients_parsed])

    # calculate cosine similarity between actual recipe ingreds and test ingreds
    cos_sim = map(lambda x: cosine_similarity(
        ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)

    # Filter top N recommendations
    recommendations = get_recommendations(N, scores)
    return recommendations


if __name__ == "__main__":
    # test ingredients
    test_ingredients = "pasta, tomato, onion"
    recs = RecSys(test_ingredients)
    print(recs.score)
