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
    # logging.warning(ingredients)

    # We need to turn output into JSON.
    recipes = {}
    for index, row in recipe.iterrows():
        # logging.warning(row)
        recipes[index] = {
            'recipe': str(row['recipe']),
            'score': float(row['score'])*100,
            'ingredients': str(row['ingredients']),
            'url': str(row['url']),
            'directions': row['directions'],
            'ctime': str(row['ctime'])
        }
    return render_template("result.html", result=recipes)


if __name__ == "__main__":
    app.run(debug=True)

# Preprocessing: getting rid of punctuation, removing accents, making everything lowercase, getting rid of Unicode, lemmatization
# Extracting Features: TF-IDF (TfidfVectorizer)
# Recommendation System: Cosine similarity

# http://127.0.0.1:5000/recipe?ingredients=%20pasta%20tomato%20onion

# Display data in result.html
# ast library error
# Take a picture of the ingredients and extract data
# Write a blog on this project
