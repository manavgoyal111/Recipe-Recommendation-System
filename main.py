from flask import Flask, render_template, jsonify, request
import json
import requests
import pickle
import pandas as pd

import sys
sys.path.append("model")
import recommendation

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    # It can be accessed by http://127.0.0.1:5000/
    return HELLO_HTML


HELLO_HTML = """
        <html><body>
            <h1>Welcome to my api: Whatscooking!</h1>
            <p>Please add some ingredients to the url to receive recipe recommendations.
                You can do this by appending "/recipe?ingredients= Pasta Tomato ..." to the current url.
            <br>Click <a href="/recipe?ingredients= pasta tomato onion">here</a> for an example when using the ingredients: pasta, tomato and onion.
        </body></html>
     """


@app.route('/recipe', methods=["GET", "POST"])
def recipe():
    ingredients = request.args.get('ingredients')
    recipe = recommendation.RecSys(ingredients)

    # We need to turn output into JSON.
    response = {}
    count = 0
    for index, row in recipe.iterrows():
        response[count] = {
            'recipe': str(row['recipe']),
            'score': str(row['score']),
            'ingredients': str(row['ingredients']),
            'url': str(row['url'])
        }
        count += 1
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

# Preprocessing: getting rid of punctuation, removing accents, making everything lowercase, getting rid of Unicode, lemmatization
# Extracting Features: TF-IDF (TfidfVectorizer)
# Recommendation System: Cosine similarity

# Take a picture of the ingredients and extract data
# Write a blog on this project
