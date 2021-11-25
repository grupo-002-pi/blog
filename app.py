from flask import Flask, render_template, request, url_for, flash, redirect
import os
import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from werkzeug.exceptions import abort


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config['SESSION_TYPE'] = 'session'
app.config['SECRET KEY'] = 'abcdefghij'
sess = Session()
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(00), nullable=False)
    content = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/duvidas')
def duvidas():
    questions = Questions.query.all()
    return render_template('duvidas.html', questions=questions)



def get_questions(questions_id):
    questions = Questions.query.filter_by(id=questions_id).first()
    if questions is None:
        abort(404)
    return questions


@app.route('/<int:questions_id>')
def questions(questions_id):
    questions = get_questions(questions_id)
    return render_template('questions.html', questions=questions)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            return redirect(url_for('error'))
        elif not content:
            return redirect(url_for('error'))
        else:
            questions = Questions(title=title, content=content)
            db.session.add(questions)
            db.session.commit()
            return redirect(url_for('duvidas'))

    return render_template('create.html')


@app.route('/<int:id>_edit', methods=('GET', 'POST'))
def edit(id):
    questions = get_questions(id)


    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            return redirect(url_for('error'))
        elif not content:
            return redirect(url_for('error'))
        else:
            questions.title = title
            questions.content = content
            db.session.commit()

            return redirect(url_for('duvidas'))

    return render_template('edit.html', questions=questions)


@app.route('/<int:id>_delete', methods=('GET', 'POST'))
def delete(id):
        questions = get_questions(id)
        db.session.delete(questions)
        db.session.commit()
        return redirect(url_for('duvidas'))

@app.route('/como_utilizar_youtube')
def ytube():
    return render_template('ytube.html')

@app.route('/como_utilizar_meet')
def meet():
    return render_template('meet.html')

@app.route('/error')
def error():
    return render_template('error_update.html')

@app.route('/como_utilizar_zoom')
def zoom():
    return render_template('zoom.html')

@app.route('/como_utilizar_whats')
def whats():
    return render_template('whats.html')

app.run()
