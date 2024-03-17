import pandas as pd
import numpy as np
import sqlite3
from ejer3 import groupByEasyCrackPass
import plotly.graph_objects as go

def printGraphic(top5WebsOutdated):
    fig = go.Figure(data=[
        go.Bar(name='Cookies', x=top5WebsOutdated['web'], y=top5WebsOutdated['cookies']),
        go.Bar(name='Aviso', x=top5WebsOutdated['web'], y=top5WebsOutdated['warning']),
        go.Bar(name='Protección de datos', x=top5WebsOutdated['web'], y=top5WebsOutdated['dataProtection'])
    ])

    # Actualizar diseño del gráfico
    fig.update_layout(barmode='group', title='Páginas web con políticas desactualizadas', xaxis_title='Páginas web',
                      yaxis_title='Número de políticas desactualizadas')

    # Mostrar el gráfico
    fig.show()


def outdatedWebs(usersDataFrame):
    # Filtrar las filas que contienen al menos una política desactualizada
    outdated = usersDataFrame[(usersDataFrame["cookies"] == 0) | (usersDataFrame["warning"] == 0) | (usersDataFrame["dataProtection"] == 0)].copy()

    # Contar la cantidad de políticas desactualizadas para cada página web
    contOutdated = outdated[['cookies', 'warning', 'dataProtection']].sum(axis=1)
    outdated.loc[:, 'desactualizadas_count'] = contOutdated

    # Ordenar las páginas web por la cantidad de políticas desactualizadas de manera descendente
    topOutdated = outdated.sort_values(by='desactualizadas_count', ascending=False)

    # Mostrar las 5 páginas web con más políticas desactualizadas
    top_5_desactualizadas = topOutdated.head(5)
    return top_5_desactualizadas[["web", "cookies", "warning", "dataProtection"]]






if __name__ =='__main__':
    con = sqlite3.connect("databaseETL.db")
    cur = con.cursor()

    usersDataFrame = pd.read_sql_query("SELECT * from legal", con)

    top5WebsOutdated = outdatedWebs(usersDataFrame)
    printGraphic(top5WebsOutdated)


    con.close()