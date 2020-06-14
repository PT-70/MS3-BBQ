import os
import json
from flask import Flask, render_template, redirect, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from os import path
if path.exists("env.py"):
  import env 

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY')

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://paulyjd:SECRET_KEY@cluster0-n4t36.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

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

@app.route('/add_task')
def add_task():
    return render_template('addtask.html')
                         


@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks =  mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    return render_template('edittask.html', task=the_task)


@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},  
  {
        'task_name':request.form.get('task_name'),
        'task_description': request.form.get('task_description'),
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)