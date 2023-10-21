import requests

# URL de la API de FastAPI
api_url = "http://127.0.0.1:8000"  # Reemplaza con la URL de tu API

# Datos de la nueva película
new_movie = {
    "id": 1,  # Reemplaza con un ID adecuado
    "title": "Nueva Película",
    "overview": "Una película emocionante",
    "year": 2022,
    "rating": 8.0,
    "category": "Acción"
}

def post_a_movie():
    # Realiza una solicitud POST para crear la película
    response = requests.post(f"{api_url}/movies", json=new_movie)

    # Verifica si la solicitud se completó con éxito
    if response.status_code == 201:
        print("Película creada exitosamente")
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")

def update_a_movie():
    # Realiza una solicitud POST para crear la película
    response = requests.put(f"{api_url}/movies/1", json=new_movie)

    # Verifica si la solicitud se completó con éxito
    if response.status_code == 200:
        print("Película modificada exitosamente")
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")

def delete_a_movie():
    # Realiza una solicitud POST para crear la película
    response = requests.delete(f"{api_url}/movies/1")

    # Verifica si la solicitud se completó con éxito
    if response.status_code == 200:
        print("Película eliminada exitosamente")
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")

# update_a_movie()
# post_a_movie()
# delete_a_movie()

from config.database import session
from app.models.movie import MovieModel
from fastapi.encoders import jsonable_encoder
db = session()
print(jsonable_encoder(db.query(MovieModel).filter(MovieModel.category == 'Accion').all()))