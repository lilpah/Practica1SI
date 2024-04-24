import sqlite3
from datetime import datetime

import pandas as pd
import numpy as np
from numpy import nan

con = sqlite3.connect("../databaseETL.db")
cur = con.cursor()



# Apartado a: Número de muestras (y campos missing o None).
usersDataFrame = pd.read_sql_query("SELECT * from users", con)
# Numero de muestras diferente a None
print(f"Número de muestras: {len(usersDataFrame.dropna())}")


# Apartado b: Media y desviación estándar del total de fechas en las que se ha cambiado la contraseña.
datesDataFrame = pd.read_sql_query("SELECT u.username, COUNT(f.fecha) AS numero_de_fechas FROM usuarios u LEFT JOIN fechas f ON u.username = f.username GROUP BY u.username", con)


datesMean = datesDataFrame.mean()
dateDv = datesDataFrame.std()
print(f'Media de cambios de contraseña: {datesMean}')
print(f'Desviación estándar de cambios de contraseña: {dateDv}')

# Apartado c: Media y desviación estándar del total de IPs que se han detectado
ipsDataFrame = pd.read_sql_query("SELECT username, ips FROM users", con)
ipsDataFrame['numIps'] = 0
i = 0
for str in ipsDataFrame['ips']:
    str = str.strip('[]').split(", ")
    ipsDataFrame.loc[i,'numIps'] = len(str)
    i+=1

ipsMean = ipsDataFrame['numIps'].mean()
ipsDv = ipsDataFrame['numIps'].std()
print(f'Media de IPs detectadas: {ipsMean}')
print(f'Desviación estándar de IPs detectadas: {ipsDv}')


# Apartado d: Media y desviación estándar del número de email recibidos de phishing en los que ha interactuado cualquier usuario.
clickedDataFrame = pd.read_sql_query("SELECT username, clickedEmails FROM users", con)

clickedMean = clickedDataFrame['clickedEmails'].mean()
clickedDv = clickedDataFrame['clickedEmails'].std()
print(f'Media de correos de phishing clickados: {clickedMean}')
print(f'Desviación estándar de correos de phishing clickados: {clickedDv}')

# Apartado e: Valor mínimo y valor máximo del total de emails recibidos.
totalEmailsDataFrame = pd.read_sql_query("SELECT username, totalEmails FROM users", con)
minEmails = totalEmailsDataFrame['totalEmails'].min()
maxEmails = totalEmailsDataFrame['totalEmails'].max()
print(f'Número mínimo de emails recibidos: {minEmails}')
print(f'Número máximo de emails recibidos: {maxEmails}')

#Apartado f: Valor mínimo y valor máximo del número de emails de phishing en los que ha interactuado un administrador.
adminDataFrame = usersDataFrame[usersDataFrame['perms']=='1']
minAdminEmails = adminDataFrame['clickedEmails'].min()
maxAdminEmails = adminDataFrame['clickedEmails'].max()
print(f'Mínimo de emails de phishing interactuados por administradores: {minAdminEmails}')
print(f'Máximo de emails de phishing interactuados por administradores: {maxAdminEmails}')


con.close()