from flask import session, render_template

from app import app


@app.route('/', methods=['GET'])
def index():
    session['token'] = 'pouet'
    return render_template('index.html')
