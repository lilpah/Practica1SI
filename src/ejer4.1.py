import ast
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import sqlite3
import plotly.graph_objects as go

from src.ejer3 import groupByEasyCrackPass

def graficopass(usersDataFrame):
    # Convertir la cadena de lista en una lista de Python
    usersDataFrame.loc[:, 'dates'] = usersDataFrame['dates'].apply(ast.literal_eval)
    # Convertir cada elemento de la lista en objeto de fecha
    usersDataFrame.loc[:, 'dates'] = usersDataFrame['dates'].apply(
        lambda x: [pd.to_datetime(date, format='%d/%m/%Y') for date in x])

    # Filtrar usuarios normales y administradores
    usuariosnormales = usersDataFrame[usersDataFrame['perms'] == '0']
    administradores = usersDataFrame[usersDataFrame['perms'] == '1']
    mediaNormal = []
    i = 0
    for dateslist in usuariosnormales['dates']:
        dateslist.sort()
        datesUser=[]
        for date in dateslist:
            datesUser.append(date)

        mediaNormal.append((np.diff(datesUser).mean()))
        i+=1


    mediaAdmin = []

    i = 0
    for dateslist in administradores['dates']:
        dateslist.sort()
        datesUser = []
        for date in dateslist:
            datesUser.append(date)

        mediaAdmin.append((np.diff(datesUser).mean()))
        i += 1

    dias_convertidos = []
    for td in mediaNormal:
        if isinstance(td, timedelta):
            dias_convertidos.append(td.days)  # Obtenemos los días
        else:
            dias_convertidos.append(np.nan)


    dias_convertidos_admin = []
    for td in mediaAdmin:
        if isinstance(td, timedelta):
            dias_convertidos_admin.append(td.days)  # Obtenemos los días
        else:
            dias_convertidos_admin.append(np.nan)

    categorias = ['Usuarios Normales', 'Administradores']
    valores = [dias_convertidos, dias_convertidos_admin]

    # Crear figura
    fig = go.Figure()

    # Añadir líneas para cada categoría
    for i in range(len(categorias)):
        fig.add_trace(go.Scatter(
            x=list(range(len(valores[i]))),
            y=valores[i],
            mode='lines+markers',
            name=categorias[i]
        ))

    # Actualizar diseño del gráfico
    fig.update_layout(
        title='Promedio de días entre fechas para Usuarios Normales y Administradores',
        xaxis_title='Índice de Valor',
        yaxis_title='Promedio de Días',
    )

    # Mostrar gráfico
    fig.show()


#easy_to_crack_users, difficult_to_crack_users = groupByEasyCrackPass(usersDataFrame)
if __name__ =='__main__':
    con = sqlite3.connect("databaseETL.db")
    cur = con.cursor()
    usersDataFrame = pd.read_sql_query("SELECT * from users", con)
    graficopass(usersDataFrame)
    con.close()