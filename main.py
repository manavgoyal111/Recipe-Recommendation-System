from flask import Flask, render_template, jsonify, request
import json
import requests
import pickle
import pandas as pd
import logging

import sys
sys.path.append("model")
import recommendation

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@app.route('/recipe', methods=["GET", "POST"])
def recipe():
    ingredients = request.args.get('ingredients')
    recipe = recommendation.RecSys(ingredients)
    # logging.warning('This is a debug message')
    # logging.warning(ingredients)

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

# http://127.0.0.1:5000/recipe?ingredients=%20pasta%20tomato%20onion

# Display data in result.html
# ast library error
# Take a picture of the ingredients and extract data
# Write a blog on this project
