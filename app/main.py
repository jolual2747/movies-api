from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
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
    db = session()
    results = db.query(MovieModel).all()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(results))

# parametro de ruta
@app.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
# parametros query
@app.get("/movies/", tags = ["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session()
    results = db.query(MovieModel).filter(MovieModel.category == category).all()
    db.close()
    if results:
        return JSONResponse(status_code=200, content=jsonable_encoder(results))
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
@app.post("/movies", tags = ["movies"], response_model=dict)
def create_movie(movie:Movie) -> dict:
    db = session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.close()
    return JSONResponse(status_code=201, content={"message":"Succesfully registered"})

@app.put("/movies/{id}", tags=["movies"], status_code=200, response_model=dict)
def update_movie(id: int, movie:Movie) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"Movie not found"})      

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    db.close()
    return JSONResponse(status_code=200, content={"message":"Succesfully updated"}) 

@app.delete("/movies/{id}", tags = ["movies"], status_code=200, response_model=dict)
def delete_movie(id:int = Path(ge=1, le=2000)) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"Movie not found"})
    
    db.delete(result)
    db.commit()
    db.close()
    return JSONResponse(status_code=200, content={"message":"Succesfully deleted"})
