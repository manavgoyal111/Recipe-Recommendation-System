# Imports
import requests
from bs4 import BeautifulSoup
import csv
import datetime
import random
import pandas as pd
import time

header = ["Number", "URL", "Title", "Cooking Time",
          "Ingredients", "Directions", "Time"]
with open('data/Recipe.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)  # creating a csv writer object
    writer.writerow(header)  # writing the fields

recipeNo = 0

for i in range(32):
    URL = f'https://www.pickuplimes.com/recipe/?page={i+1}'

    # Fetching html from the website
    page = requests.get(URL)
    # BeautifulSoup enables to find the elements/tags in a webpage
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup)

    # Get all Links
    allLinks = []
    for link in soup.find_all('a'):
        if (link.get('href') and link.get('href') != '#' and link.get('href').startswith('/recipe/') and not (link.get('href') == "/recipe/latest-rss") and not (link.get('href') == "/recipe/")):
            linkText = "https://www.pickuplimes.com" + link.get('href')
            allLinks.append(linkText)
            # print(linkText)
    # print(allLinks)

    for url in allLinks:
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        title = soup.find("h1").text.strip()

        cookingtime = soup.find(
            attrs={"style": "font-weight: 400;"}).getText()

        ingredients = []
        allIn = soup.find_all(class_="ingredient-container")
        for ingre in allIn:
            inData = ingre.text.strip().replace("\n", " ")
            ingredients.append(inData)
        # for li in soup.select(‘.ingred-list li’):
        #     ingred = ‘ ‘.join(li.text.split())
        #     ingredients.append(ingred)

        directions = []
        allSteps = soup.find_all(attrs={"class": "direction"})
        for step in allSteps:
            directions.append(step.getText())

        today = datetime.date.today()  # Create a Timestamp

        recipeNo = recipeNo + 1

        data = [recipeNo, url, title, cookingtime,
                ingredients, directions, today]
        # print(data)

        with open('data/Recipe.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)  # creating a csv writer object
            writer.writerow(data)  # appending the new row

    print(f"Done for page {i}")
    time.sleep(random.randint(5, 10, 1))
