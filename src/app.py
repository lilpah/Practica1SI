#!/usr/bin/env python3
import sqlite3
from src.hashSHA256 import hashSHA256
import numpy as np
from flask import Flask, render_template, request, redirect
from sklearn.linear_model import LinearRegression

from src.vulnerabilidades import obtener_ultimas_vulnerabilidades
from src.modelos import prediccion, linearRegresion

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

@app.errorhandler(500)
def internal_server_error(e):
    return "Ha ocurrido un error. Por favor, intentalo de nuevo.", 500


@app.route("/top10")
def top10():
    ultimas_vulnerabilidades = obtener_ultimas_vulnerabilidades()
    if ultimas_vulnerabilidades is not None:
        return render_template("top10.html", app_data=app_data, ultimas_vulnerabilidades=ultimas_vulnerabilidades)
    else:
        return "Error al obtener las últimas vulnerabilidades.", 500




@app.route("/analisisMetricas")
def ejercicio2():
    return render_template("analisisMatricas.html", app_data=app_data)

@app.route("/topXcriticalUsers",methods = ['POST'])
def topXcriticalUsers():
    if request.method == 'POST':
       try:
            number = request.form['number']
            opcion = request.form['outputType']
            con = sqlite3.connect('databaseETL.db')
            cursorObj = con.cursor()

            cursorObj.execute('''SELECT username,(clickedEmails*100/phishingEmails) AS percentaje FROM users  ORDER BY percentaje DESC LIMIT ? ''',(number,))

            users = cursorObj.fetchall()
            userfinal = []

            if opcion == 'normal':
                for (user,percentaje) in users:
                    userfinal.append(user)
            elif opcion == 'mayor':
                for (user,percentaje) in users:
                    if percentaje >= 50:
                        userfinal.append(user)
            elif opcion == 'menor':
                for (user,percentaje) in users:
                    if percentaje < 50:
                        userfinal.append(user)

            con.close()
            return render_template('topXcriticalUsers.html', app_data=app_data,number=number, users=userfinal)
       except Exception as e:
            app.logger.error('Ocurrió un error en la consulta: %s', str(e))
            return "Ha ocurrido un error. Por favor, intentalo de nuevo.", 500



@app.route("/loginPage")
def loginPage():
    return render_template("login.html", app_data=app_data)

@app.route("/signInPage")
def signInPage():
    return render_template("signIn.html", app_data=app_data)
@app.route("/signIn", methods = ['POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = hashSHA256(password)
        con = sqlite3.connect('databaseETL.db')
        cursorObj = con.cursor()
        try:
            cursorObj.execute('''INSERT INTO usersLogin VALUES (?,?)''',
                      (username, hashedPassword))
            con.commit()
            con.close()
        except Exception as e:
            app.logger.error('Ocurrió un error en la consulta: %s', str(e))
            return "Usuario ya registrado. Cambie de nombre de usuario o inicie sesión.", 500
        return redirect('/loginPage')

@app.route("/login",methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = hashSHA256(password)
        con = sqlite3.connect('databaseETL.db')
        cursorObj = con.cursor()
        try:
            cursorObj.execute(
                '''SELECT username,password FROM usersLogin WHERE username = ? ''',
                (username,))
            users = cursorObj.fetchall()

            (name, passwd) = users[0]
            if password == passwd:
                return render_template("userPage.html", app_data=app_data, username=username)
            else:
                return redirect("/loginPage")
        except Exception as e:
            app.logger.error('Ocurrió un error en la consulta: %s', str(e))
            return "Usuario o contraseña incorrectos. Porfavor vuelva a iniciar sesión", 500


@app.route("/modelosIA",methods = ['POST'])
def modelosIA():
    if request.method == 'POST':
        try:
            name = request.form['name']
            totalEmails = request.form['totalEmails']
            phishingEmails = request.form['phishingEmails']
            clickedEmails = request.form['clickedEmails']
            modelo = request.form['outputType']

            if modelo == 'regLineal':
                model = linearRegresion()
                valorPredecir = [float(clickedEmails) / float(phishingEmails)]
                valorPredecir = np.array([valorPredecir])
                result = prediccion(model, valorPredecir)

            return render_template("resultModelos.html", app_data=app_data, name=name, result=result)
        except Exception as e:
            app.logger.error('Ocurrió un error inesperado: %s', str(e))
            return "Ha ocurrido un error. Por favor, intentalo de nuevo.", 500

@app.route("/modelosSupervisados")
def modelosSupervisados():
    return render_template("modelosIA.html", app_data=app_data)
if __name__ == "__main__":

    app.run(debug=DEVELOPMENT_ENV)
