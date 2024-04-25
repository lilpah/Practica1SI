import sqlite3
import subprocess
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn import tree
import graphviz
from sklearn.tree import export_graphviz, DecisionTreeClassifier
from subprocess import call
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier





def linearRegresion():
    # Conectar a la base de datos
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    # Crear la característica X como la combinación de clickedEmails / phishingEmails
    usersDataFrame['x'] = usersDataFrame['clickedEmails'] / usersDataFrame['phishingEmails']

    # Crear un imputador para reemplazar los valores NaN con la media
    imputer = SimpleImputer(strategy='mean')
    usersDataFrame['x'] = imputer.fit_transform(usersDataFrame[['x']])

    # Seleccionar la nueva característica X y la variable de destino y
    X = np.array(usersDataFrame[['x']])
    y = np.array(usersDataFrame['critical'])

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=33)

    # Crear el modelo de regresión lineal
    modelLinReg = LinearRegression()

    # Entrenar el modelo con los datos de entrenamiento
    modelLinReg.fit(X_train, y_train)

    """     
    ############## Todo esto mostrado en la memoria ##############
    
    ####### Predecir
    y_pred = modelLinReg.predict(x_test)
    
    ####### Calcular pendiente
    m = modelLinReg.coef_

    ####### Printear la pendiente
    print("Pendiente ", m)

    ####### Calcular el error cuadratico
    squarredError = mean_squared_error(y_test, y_pred)
    print("Mean squared error:", squarredError)

    ####### Mostrar graficamente
    plt.scatter(x_test, y_test, color="black")
    plt.plot(x_test, y_pred, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()
    """

    return modelLinReg


def decisionTree():
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT totalEmails, clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    #Dividie los datos
    x = np.array(usersDataFrame[['totalEmails', 'phishingEmails', 'clickedEmails']])
    y = np.array(usersDataFrame['critical'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)

    # Arbol de decision
    decTree = tree.DecisionTreeClassifier()

    #Entrenamos modelo
    decTree = decTree.fit(x_train, y_train)

    """
    ############## Todo esto mostrado en la memoria ##############
    
    ####### Predecir
    predY = decTree.predict(x_test)
   
    ######## Calculamos la exactitud del modelo
    accuracy = accuracy_score(y_test, predY)
    print("Accuracy:", accuracy)
   

    ####### Representacion grafica
    feature_names = ['totalEmails', 'phishingEmails', 'clickedEmails']
    class_names = ['non_critical', 'critical']

    dot_data = tree.export_graphviz(decTree, out_file=None,
                                    feature_names=feature_names,
                                    class_names=class_names,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render('criticidadUsuarios.gv', view=True).replace('\\', '/')
    """

    return decTree


def randomForest():
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT totalEmails, clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    # Dividie los datos
    x = np.array(usersDataFrame[['totalEmails', 'phishingEmails', 'clickedEmails']])
    y = np.array(usersDataFrame['critical'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)


    ranForest = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=15)
    ranForest.fit(x_train, y_train)


    """
    ############## Todo esto mostrado en la memoria ##############
    
    ####### Predecir utilizando el conjunto de prueba
    predY = ranForest.predict(x_test)

    ####### Calcular la precisión del modelo
    accuracy = accuracy_score(y_test, predY)
    print("Accuracy:", accuracy)

    ####### Muestro todos los subarboles del forest en el directorio randomForest
    feature_names = ['totalEmails', 'phishingEmails', 'clickedEmails']
    class_names = ['non_critical', 'critical']
    for i in range(len(ranForest.estimators_)):
        print(i)
        estimator = ranForest.estimators_[i]
        export_graphviz(estimator,
                        out_file='randomTree/tree.dot',
                        feature_names=feature_names,
                        class_names=class_names,
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        call(['dot', '-Tpng', 'tree.dot', '-o', 'randomTree/' + 'tree' + str(i) + '.png', '-Gdpi=600'])
    """

    return ranForest


# Modelo nuevo implementado para el ejercicio 4
# Modelo KNN (K-Nearest Neighbors)
def knn_model():
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT totalEmails, clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    # Dividir los datos
    x = np.array(usersDataFrame[['totalEmails', 'phishingEmails', 'clickedEmails']])
    y = np.array(usersDataFrame['critical'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)

    # Crear el modelo de KNN
    knn_model = KNeighborsClassifier(n_neighbors=10)

    # Entrenar el modelo
    knn_model.fit(x_train, y_train)

    """
    pred_y = knn_model.predict(x_test)

    # Calcular la precisión del modelo
    accuracy = accuracy_score(y_test, pred_y)
    print("Accuracy:", accuracy)
    """

    # Devolver el modelo entrenado
    return knn_model



def prediccion(model, user):
    if isinstance(model, LinearRegression):
        # Realizar predicción utilizando el modelo de regresión lineal
        predY = model.predict(user)
        m = model.coef_

        # Si la prediccion es menor que la pendiente -> usuario no critico
        if predY < m:
            return " no critico"
        else:
            return " critico"
    elif isinstance(model, DecisionTreeClassifier):
        # Realizar predicción utilizando el modelo de árbol de decisión
        predY = model.predict(user)

        # Si la prediccion es 1 -> usuario crtico
        if predY == 1:
            return " critico"
        else:
            return " no critico"
    elif isinstance(model, RandomForestClassifier):
        # Realizar predicción utilizando el modelo de bosque aleatorio
        predY = model.predict(user)

        # Si la prediccion es 1 -> usuario crtico
        if predY == 1:
            return " critico"
        else:
            return " no critico"
    elif isinstance(model, KNeighborsClassifier):
        # Realizar predicción utilizando el modelo de bosque aleatorio
        predY = model.predict(user)

        # Si la prediccion es 1 -> usuario crtico
        if predY == 1:
            return " critico"
        else:
            return " no critico"
    else:
        print("Modelo no válido")
        return None



if __name__ == '__main__':

    ############ Probar los modelos por consola de forma independiente

    # Modelo regresion lineal
    dataRegresionLineal = [1.93]
    dataRegresionLineal = np.array([dataRegresionLineal])
    linReg = linearRegresion()

    usuario1 = prediccion(linReg, dataRegresionLineal)
    print(usuario1)


    # Modelo decision tree
    decision = decisionTree()
    dataDecision = [145, 11, 566]
    dataDecision = np.array([dataDecision])

    usuario2 = prediccion(decision, dataDecision)
    print(usuario2)

    # Modelo random forest
    random = randomForest()
    dataRandom = [145, 11, 566]
    dataRandom = np.array([dataRandom])

    usuario3 = prediccion(random, dataRandom)
    print(usuario3)

    # Modelo KNN
    uda = knn_model()
    dataRandom = [145, 11, 566]
    dataRandom = np.array([dataRandom])

    usuario4 = prediccion(uda, dataRandom)
    print(usuario4)


