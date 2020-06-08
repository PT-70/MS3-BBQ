import os
import json
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grills')
def grills():
    data = []
    with open('data/grills.json', 'r') as json_data:
        data = json.load(json_data)
    return render_template('grills.html', page_title="What's the right Grill for me?", grills=data)


@app.route('/recipes')
def recipes():
    data = []
    with open('data/recipes.json', 'r') as json_data:
        data = json.load(json_data)
    return render_template('recipes.html', page_title='Simple recipes that will make you look like a pro!', recipes=data)


@app.route('/recipes/<recipes_name>')
def recipes_recipes(recipes_name):
    recipes = {}

    with open('data/recipes.json', 'r') as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj['url'] == recipes_name:
                recipes = obj

    return '<h1>' + recipes['ingredients'] + '</h1>'

@app.route('/tips')
def tips():
    data = []
    with open('data/tips.json', 'r') as json_data:
        data = json.load(json_data)
    return render_template('tips.html', page_title="FAQ'S", tips=data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thanks {}, We have received your message'.format(request.form['name']))
    return render_template('contact.html', page_title='Contact')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)