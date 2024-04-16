import json
import sqlite3
from datetime import datetime


def createBBDD():
    # Conexion a la base de datos creada (databaseETL.db)
    conn = sqlite3.connect('databaseETL.db')
    c = conn.cursor()

    # Creamos las tablas usuarios y legal
    c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, phone INTEGER, password TEXT, province TEXT, perms TEXT, totalEmails INTEGER, phishingEmails INTEGER, clickedEmails INTEGER, critical INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS legal
                     (web TEXT PRIMARY KEY, cookies INTEGER, warning INTEGER, dataProtection INTEGER,  createNumber INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS usersDatesIps
                         (username TEXT , dates DATE, ip TEXT,FOREIGN KEY (username) REFERENCES users(username),PRIMARY KEY (username, dates,ip))''')

    # Confirmamos cambios y cerramos la conexion
    conn.commit()
    conn.close()

def insertUsers(userFile):
    # Conexion a la BBDD
    conn = sqlite3.connect('databaseETL.db')
    c = conn.cursor()

    # Abrimos el fichero cargando su contendio en data
    with open(userFile, 'r') as f:
        data = json.load(f)

    # Metemos los datos en la tabla users

    for user in data['usuarios']:
        for dataOfUser in user.values():
            username = list(user.keys())[0]
            phone = dataOfUser['telefono']
            password = dataOfUser['contrasena']
            province = dataOfUser['provincia']
            perms = dataOfUser['permisos']
            totalEmails = dataOfUser['emails']['total']
            phishingEmails = dataOfUser['emails']['phishing']
            clickedEmails = dataOfUser['emails']['cliclados']
            dates = (dataOfUser['fechas'])
            ips = (dataOfUser['ips'])
            critical = (dataOfUser['critico'])

            maxNum = max(len(dates),len(ips))
            minNum = min(len(dates),len(ips))
            for cont in range(maxNum):


                fecha = datetime.strptime(dates[cont], '%d/%m/%Y').date()
                if ips != 'None':
                    ip = ips[cont]
                else:
                    ip = "None"
                c.execute('''INSERT OR IGNORE INTO usersDatesIps VALUES (?, ?, ?)''',
                          (username, fecha, ip))


            c.execute('''INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (username, phone, password, province, perms, totalEmails, phishingEmails, clickedEmails, critical))

    # Confirmamos cambios y cerramos la conexion
    conn.commit()
    conn.close()


def insertLegal(legalFile):
    conn = sqlite3.connect('databaseETL.db')
    c = conn.cursor()

    # Open JSON file and load data
    with open(legalFile, 'r') as f:
        data = json.load(f)

    # Insert data into tables
    for webs in data['legal']:
        for dataOfWeb in webs.values():
            web = list(webs.keys())[0]
            cookies = dataOfWeb['cookies']
            warning = dataOfWeb['aviso']
            dataProtection = dataOfWeb['proteccion_de_datos']
            createNumber = dataOfWeb['creacion']

            c.execute('''INSERT OR IGNORE INTO legal VALUES (?, ?, ?, ?, ?)''',
                      (web, cookies, warning, dataProtection, createNumber))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Creando base de datos...")
    createBBDD()
    print("[!] BBDD creada")
    print("Insertando datos de users_data_online.json y legal_data_online.json")
    insertUsers("ficheros/users_data_online_clasificado.json")
    insertLegal("ficheros/legal_data_online.json")
    print("Base de datos creada correctamente")


   