import sqlite3
from datetime import datetime

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
datesDataFrame['numDates'] = 0
i = 0
for str in datesDataFrame['dates']:
    str = str.strip('[]').split(", ")
    datesDataFrame.loc[i,'numDates'] = len(str)
    i+=1

print(datesDataFrame)
datesMean = datesDataFrame['numDates'].mean()
dateDv = datesDataFrame['numDates'].std()
print(f'Media de cambios de contraseña: {datesMean}')
print(f'Desviación estándar de cambios de contraseña: {dateDv}')

con.close()