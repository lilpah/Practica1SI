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
from sklearn.tree import export_graphviz
from subprocess import call



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
    X = usersDataFrame[['x']]
    y = usersDataFrame['critical']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=33)

    # Crear el modelo de regresión lineal
    modelLinReg = LinearRegression()

    # Entrenar el modelo con los datos de entrenamiento
    modelLinReg.fit(X_train, y_train)

    # Obtener la pendiente del modelo
    pendiente = modelLinReg.coef_[0]


    # Inicializar y_pred
    y_pred = modelLinReg.predict(x_test)

    """
    y_pred = []
    # Asignar valores a y_pred según la pendiente
    for val in x_test['x']:
        if val < pendiente:
            y_pred.append(0)
        else:
            y_pred.append(1)
    """
    
    # Printear la pendiente
    print("Pendiente ", modelLinReg.coef_)
    
    # Calcular el score de y_test y de y_pred
    score = mean_squared_error(y_test, y_pred)
    print("x_test", x_test)
    print("y_test: ", y_test)
    print("y_pred: ", y_pred)
    
    print("Mean squared error:", score)


    plt.scatter(x_test, y_test, color="black")
    plt.plot(x_test, y_pred, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()


def decisionTree():
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT totalEmails, clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    #Dividie los datos
    x = usersDataFrame[['totalEmails', 'phishingEmails', 'clickedEmails']]
    y = usersDataFrame['critical']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)


    # Arbol de decision
    decTree = tree.DecisionTreeClassifier()
    decTree = decTree.fit(x_train, y_train)


    predY = decTree.predict(x_test)
    # Calculamos la exactitud del modelo
    accuracy = accuracy_score(y_test, predY)
    print("Accuracy:", accuracy)

    feature_names = ['totalEmails', 'phishingEmails', 'clickedEmails']
    class_names = ['non_critical', 'critical']

    dot_data = tree.export_graphviz(decTree, out_file=None,
                                    feature_names=feature_names,
                                    class_names=class_names,
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render('criticidadUsuarios.gv', view=True).replace('\\', '/')


def randomForest():
    con = sqlite3.connect("databaseETL.db")

    # Leer datos de la tabla 'users' en un DataFrame
    usersDataFrame = pd.read_sql_query("SELECT totalEmails, clickedEmails, phishingEmails, critical FROM users", con)

    # Cerrar la conexión a la base de datos
    con.close()

    # Dividie los datos
    x = usersDataFrame[['totalEmails', 'phishingEmails', 'clickedEmails']]
    y = usersDataFrame['critical']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)


    ranForest = RandomForestClassifier(max_depth=2, random_state=0,n_estimators=10)
    ranForest.fit(x_train, y_train)




    # Predecir utilizando el conjunto de prueba
    predY = ranForest.predict(x_test)
    """
    uda = [256, 65, 12]
    uda_matriz = np.array([uda])
    predY = ranForest.predict(uda_matriz)
    print(uda_matriz)
    print(predY)

    """




    # Calcular la precisión del modelo
    accuracy = accuracy_score(y_test, predY)
    print("Accuracy:", accuracy)

    """
    print(x_test)
    print(y_test)
    print(predY)
    """

    # Muestro todos los subarboles del forest en el directorio randomForest
    feature_names = ['totalEmails', 'phishingEmails', 'clickedEmails']
    class_names = ['non_critical', 'critical']
    for i in range(len(ranForest.estimators_)):
        print(i)
        estimator = ranForest.estimators_[i]
        export_graphviz(estimator,
                        out_file='tree.dot',
                        feature_names=feature_names,
                        class_names=class_names,
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        call(['dot', '-Tpng', 'tree.dot', '-o', 'randomTree/' + 'tree' + str(i) + '.png', '-Gdpi=600'])



if __name__ == '__main__':
    #linearRegresion()
    #decisionTree()
    randomForest()



