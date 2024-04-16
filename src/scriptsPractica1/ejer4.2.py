import pandas as pd
import numpy as np
import sqlite3
from ejer3 import groupByEasyCrackPass
import plotly.graph_objects as go

def printGraphic(top10Users):
    # Crear la figura
    fig = go.Figure()

    # Agregar los datos como una serie de barras horizontales
    fig.add_trace(go.Bar(
        x=top10Users['clickedEmails'],
        y=top10Users['username'],
        orientation='h',  # Orientación horizontal de las barras
        marker=dict(color='blue')  # Color de las barras
    ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        title='Top 10 usuarios con mayor número de correos electrónicos clicados',
        xaxis_title='Número de correos electrónicos clicados',
        yaxis_title='Nombre de usuario',
        yaxis=dict(autorange='reversed')  # Invertir el eje y para que los nombres aparezcan en orden descendente
    )

    # Mostrar el gráfico
    fig.show()


def tenUsersMostCritics(usersDataFrame):
    # Reutilizamos la funcion del ejercicio 3 que creamos para agrupar los usuarios con contraseñas mas debiles
    usersEasyToCrack, usersDifficultToCrack = groupByEasyCrackPass(usersDataFrame)

    # En este caso simplemente necesitamos los usuarios cuyas contraseñas son mas debiles (usersEasyToCrack)
    # Podemos ordenar los usuarios por el campo de clickedEmails, por lo que tendremos ordenados de mayor a menor segun el numero
    # de veces que se hay clickado un correo
    users_sorted = usersEasyToCrack.sort_values(by='clickedEmails', ascending=False)

    # Nos quedamos con los 10 primeros usuarios
    top_10_users = users_sorted.head(10)

    #print(top_10_users[['username', 'clickedEmails']])
    return top_10_users[['username', 'clickedEmails']]



if __name__ =='__main__':
    con = sqlite3.connect("../databaseETL.db")
    cur = con.cursor()

    usersDataFrame = pd.read_sql_query("SELECT * from users", con)

    top10Users = tenUsersMostCritics(usersDataFrame)
    printGraphic(top10Users)


    con.close()