#!/usr/bin/env python3
import sqlite3

from flask import Flask, render_template, request


DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Practica2 Sistemas de Informacion",
    "description": "Creacion de Cuadro de Mando Integral (CMI).",
    "html_title": "CMI",
    "project_name": "Nuestro CMI",
    "keywords": "flask, webapp, CMI",
}



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
        con = sqlite3.connect('databaseETL.db')
        cursorObj = con.cursor()
        cursorObj.execute('''SELECT username FROM users WHERE critical = 1 LIMIT ? ''',(number,))

        users = cursorObj.fetchall()
        con.close()
        return render_template('topXcriticalUsers.html', app_data=app_data,number=number, users = users)




if __name__ == "__main__":

    app.run(debug=DEVELOPMENT_ENV)
