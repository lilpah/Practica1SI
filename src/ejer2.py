import sqlite3
import pandas as pd
import numpy as np
from numpy import nan

con = sqlite3.connect("databaseETL.db")
cur = con.cursor()



# Apartado a: Número de muestras (y campos missing o None).
usersDataFrame = pd.read_sql_query("SELECT * from users", con)
# Numero de muestras diferente a None
print(f"Número de muestras: {len(usersDataFrame.dropna())}")


# Apartado b: Media y desviación estándar del total de fechas en las que se ha cambiado la contraseña.

datesDataFrame = pd.read_sql_query("SELECT username, dates FROM users", con)
#datesDataFrame['dates'] = pd.to_datetime(datesDataFrame['dates'])
datesDataFrameByUser = datesDataFrame.groupby('username')['dates'].nunique()
datesMean = datesDataFrame.mean()
datesDes = datesDataFrame.std()
print(f'Media de cambios de contraseña: {datesMean}')
print(f'Desviación estándar de cambios de contraseña: {datesDes}')

con.close()