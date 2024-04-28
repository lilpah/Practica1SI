import requests


def obtener_ultimas_vulnerabilidades():
    try:
        # Hacer una solicitud GET a la API para obtener las últimas vulnerabilidades
        response = requests.get("https://cve.circl.lu/api/last/")

        # Verificar la solicitud
        if response.status_code == 200:
            # Obtener los datos JSON de la respuesta
            data = response.json()
            # Filtrar las últimas 10 vulnerabilidades
            ultimas_10_vulnerabilidades = data[:10]
            return ultimas_10_vulnerabilidades
        else:
            # Si la solicitud no fue exitosa, devolver None
            return None
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la solicitud
        print(f"Error al obtener las vulnerabilidades: {e}")
        return None
