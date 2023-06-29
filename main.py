from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api', methods=['GET', 'POST'])
def qa():
    data = ""
    if request.method == 'POST':
        return jsonify(data)
    return jsonify(data)


app.run(debug=True)

# K-Nearest Neighbors algorithm

# Take a picture of the ingredients and extract data
# Write a blog on this project
