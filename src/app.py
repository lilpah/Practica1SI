#!/usr/bin/env python3
from flask import Flask, render_template, request
import SQLAlchemy

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'databaseETL.db'
db = SQLAlchemy(app)

app_data = {
    "name": "Practica2 Sistemas de Informacion",
    "description": "Creacion de Cuadro de Mando Integral (CMI).",
    "html_title": "CMI",
    "project_name": "Nuestro CMI",
    "keywords": "flask, webapp, CMI",
}

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(100), primary_key=True)
    phone = db.Column(db.Integer)
    password = db.Column(db.String(100))
    province = db.Column(db.String(100))
    perms = db.Column(db.String(100))
    totalEmails = db.Column(db.Integer)
    phishingEmails = db.Column(db.Integer)
    clickedEmails = db.Column(db.Integer)
    critical = db.Column(db.Integer)


@app.route("/")
def index():

    return render_template("index.html", app_data=app_data)


@app.route("/top10")
def top10():
    return render_template("top10.html", app_data=app_data)


@app.route("/ejercicio1.html")
def service():
    return render_template("ejercicio1.html", app_data=app_data)


@app.route("/ejercicio2")
def ejercicio2():
    return render_template("ejercicio2.html", app_data=app_data)

@app.route("/topXcriticalUsers",methods = ['POST'])
def topXcriticalUsers():
    if request.method == 'POST':
        number = request.form['number']
        users = User.query.filter_by(critical=1).order_by(User.totalEmails.desc()).limit(number).all()

        return render_template('topXcriticalUsers.html', app_data=app_data,number=number, users = users)




if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
