#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Peter Simeth's basic flask pretty youtube downloader (v1.3)
https://github.com/petersimeth/basic-flask-template
© MIT licensed, 2018-2023
"""

from flask import Flask, render_template

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


@app.route("/service")
def service():
    return render_template("service.html", app_data=app_data)


@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=app_data)




if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
