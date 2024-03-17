import hashlib
import sqlite3
import pandas as pd

def groupByPerms(usersDataFrame):
    #### Agrupcacion por tipo de permisos de usuario

    # Creo una agrupacion basandome en sus permisos 0 -> usuario normal / 1 -> administrador
    groupPerms = usersDataFrame.groupby('perms')

    # Almaceno los usuarios normales
    groupNormalUsers = groupPerms.get_group("0")

    # Almaceno los usuarios con permisos de administracion
    groupAdmins = groupPerms.get_group("1")

    """
    print("Usuarios normales\n")
    print(groupNormalUsers)
    print("Administradores\n")
    print(groupAdmins)
    """
    return groupNormalUsers, groupAdmins


def crackeable(password):

    # Abrimos el fichero cargando su contendio en data
    with open("SmallRockYou.txt", 'r') as rockYou:
        data = rockYou.read().splitlines()
        #print(data)

    # Hasheo cada password de la wordlist y si coincide con el hash es que es facilmente crackeable (Devuelvo True)
    for passwordToTry in data:
        if hashlib.md5(passwordToTry.encode()).hexdigest() == password:
            return True
    return False


def groupByEasyCrackPass(usersDataFrame):
    #### Agrupcacion por facilidad de crackeo de su contraseña

    # Creo una columna mas en la DataFrame que se llaama easyToCrack y que se pone a True o False dependiendo del resultado que retorne la funcion crackeable
    usersDataFrame['easyToCrack'] = usersDataFrame['password'].apply(crackeable)

    #Creo una agrupacion basandome en si la contraseña es facilmente crackeable o no
    usersByCrackeability = usersDataFrame.groupby('easyToCrack')

    # Almaceno los usuarios con contraseña debiles
    usersEasyToCrack = usersByCrackeability.get_group(True)

    # Almaceno los usuarios con contraseña mas robustas
    usersDifficultToCrack = usersByCrackeability.get_group(False)
    """
    print("Usuarios faciles de crackear")
    print(usersEasyToCrack)

    print("Usuarios dificiles de crackear")
    print(usersDifficultToCrack)
    """
    return usersEasyToCrack, usersDifficultToCrack



if __name__ == '__main__':

    #Conexion a la BBDD
    con = sqlite3.connect("databaseETL.db")
    cur = con.cursor()

    # Creo un DataFrame con pandas
    usersDataFrame = pd.read_sql_query("SELECT * from users", con)

    # Creo una agrupacion basada en permisos de los usuarios
    groupNormalUsers, groupAdmins = groupByPerms(usersDataFrame)

    # Creo una agrupacion basandome en si una contraseña es facilmente crackeable o no
    usersEasyToCrack, usersDifficultToCrack = groupByEasyCrackPass(usersDataFrame)