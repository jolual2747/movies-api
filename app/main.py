from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.models.movie import Movie, MovieModel
from app.models.user import User
from app.auth.jwt_manager import create_token, JWTBearer
from typing import List
from config.database import session, engine, base

app = FastAPI()

app.title = "App para Movies"
app.version = "0.0.1"

base.metadata.create_all(bind = engine)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven los Na"vi, seres que ...',
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción' 
    },
    {
        'id': 1,
        'title': 'Avatar',
        'overview': 'En un exuberante planeta llamado Pandora viven los Na"vi, seres que ...',
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción' 
    } 
]

@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world</h1>")

@app.post('/login', tags = ["auth"])
def login(user:User):
    if user.email == 'admin@gmail.com' and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)

@app.get("/movies", tags = ["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

# parametro de ruta
@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = [item for item in movies if item["id"] == id][0]
    if movie:
        return JSONResponse(status_code=200, content=movie)
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
# parametros query
@app.get("/movies/", tags = ["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movies_to_return = [item for item in movies if item["category"] == category]
    if movies_to_return:
        return JSONResponse(status_code=200, content=movies_to_return)
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
@app.post("/movies", tags = ["movies"], response_model=dict)
def create_movie(movie:Movie) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(status_code=201, content={"message":"Succesfully registered"})

@app.put("/movies/{id}", tags=["movies"], status_code=200, response_model=dict)
def update_movie(id: int, movie:Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message":"Succesfully updated"})
        else:
            return JSONResponse(status_code=404, content={"message":"Movie not found"})    

@app.delete("/movies/{id}", tags = ["movies"], status_code=200, response_model=dict)
def delete_movie(id:int = Path(ge=1, le=2000)) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message":"Succesfully deleted"})
        else:
            return JSONResponse(status_code=404, content={"message":"Movie not found"})