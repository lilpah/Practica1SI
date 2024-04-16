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
    with open("../ficheros/SmallRockYou.txt", 'r') as rockYou:
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


def calculateMedia(agrup):
    mean = agrup["phishingEmails"].mean()
    return mean


def calculateVar(agrup):
    var = agrup["phishingEmails"].var()
    return var

def calculateMaxandMin(agrup):
    max = agrup["phishingEmails"].max()
    min = agrup["phishingEmails"].min()
    return max, min

def calculateMedian(agrup):
    median = agrup["phishingEmails"].median()
    return median

def calculateNumObserv(agrup):
    sumTotal = agrup["phishingEmails"].sum()
    return sumTotal


def calculateNumValoresAusente(agrup):
    # Con esta linea cuento los campos de email de phishing que estan a 0 o con valor None
    numMissingValues = ((agrup["phishingEmails"] == 0) | (agrup["phishingEmails"].isnull())).sum()
    return numMissingValues



if __name__ == '__main__':

    #Conexion a la BBDD
    con = sqlite3.connect("../databaseETL.db")
    cur = con.cursor()

    # Creo un DataFrame con pandas
    usersDataFrame = pd.read_sql_query("SELECT * from users", con)

    # Creo una agrupacion basada en permisos de los usuarios
    groupNormalUsers, groupAdmins = groupByPerms(usersDataFrame)

    # Creo una agrupacion basandome en si una contraseña es facilmente crackeable o no
    usersEasyToCrack, usersDifficultToCrack = groupByEasyCrackPass(usersDataFrame)


    # Numero de observaciones (total de emails de phishing) de los usuarios por agrupaciones
    print("### Numero observaciones ###")
    print("El numero de observaciones de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateNumObserv(groupNormalUsers)))
    print("El numero de observaciones de emails de phishing para la agrupacion de administradores es: " + str(calculateNumObserv(groupAdmins)))
    print("El numero de observaciones de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateNumObserv(usersEasyToCrack)))
    print("El numero de observaciones de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateNumObserv(usersDifficultToCrack)) + "\n")

    print("###################\n")

    # Numero de valores ausentes (estan a 0 o a None) de los usuarios por agrupaciones
    print("### Numero valores ausentes ###")
    print("El numero de valores ausentes de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateNumValoresAusente(groupNormalUsers)))
    print("El numero de valores ausentes de emails de phishing para la agrupacion de administradores es: " + str(calculateNumValoresAusente(groupAdmins)))
    print("El numero de valores ausentes de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateNumValoresAusente(usersEasyToCrack)))
    print("El numero de valores ausentes de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateNumValoresAusente(usersDifficultToCrack)) + "\n")

    print("###################\n")

    # Mediana de emails de phishing de los usuarios por agrupaciones
    print("### Mediana ###")
    print("La mediana de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateMedian(groupNormalUsers)))
    print("La mediana de emails de phishing para la agrupacion de administradores es: " + str(calculateMedian(groupAdmins)))
    print("La mediana de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateMedian(usersEasyToCrack)))
    print("La mediana de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateMedian(usersDifficultToCrack)) + "\n")


    # Medias de emails de phishing de los usuarios por agrupaciones
    print("### Medias ###")
    print("La media de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateMedia(groupNormalUsers)))
    print("La media de emails de phishing para la agrupacion de administradores es: " + str(calculateMedia(groupAdmins)))
    print("La media de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateMedia(usersEasyToCrack)))
    print("La media de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateMedia(usersDifficultToCrack)) + "\n")

    print("###################\n")

    # Varianza de emails de phishing de los usuarios por agrupaciones
    print("### Varianzas ###")
    print("La varianza de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateVar(groupNormalUsers)))
    print("La varianza de emails de phishing para la agrupacion de administradores es: " + str(calculateVar(groupAdmins)))
    print("La varianza de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateVar(usersEasyToCrack)))
    print("La varianza de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateVar(usersDifficultToCrack)) + "\n")

    print("###################\n")

    # Valor minimo y maximo de emails de phishing de los usuarios por agrupaciones
    print("### Valores maximo y minimo ###")
    print("El valor maximo y minimo de emails de phishing para la agrupacion de usuarios normales es: " + str(calculateMaxandMin(groupNormalUsers)))
    print("El valor maximo y minimo de emails de phishing para la agrupacion de administradores es: " + str(calculateMaxandMin(groupAdmins)))
    print("El valor maximo y minimo de emails de phishing para la agrupacion de usuarios con contraseña facilmente crackeable es: " + str(calculateMaxandMin(usersEasyToCrack)))
    print("El valor maximo y minimo de emails de phishing para la agrupacion de usuarios con contraseña mas robustas es: " + str(calculateMaxandMin(usersDifficultToCrack)) + "\n")