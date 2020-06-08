import os 
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html', page_title='Simple recipes to make you look like a pro!')

@app.route('/contact')
def contact():
    return render_template('contact.html', page_title='Contact us')

@app.route('/grills')
def contact():
    return render_template('grills.html', page_title='What grill should I get?')

@app.route('/tips')
def contact():
    return render_template('tips.html', page_title='FAQ')

    if __name__ == '__main__':
        app.run(host=os.environ.get('IP'),
                port=int(os.environ.get('PORT')),
                debug=True)
    