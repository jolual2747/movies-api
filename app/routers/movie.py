from typing import List
from fastapi import APIRouter, Depends, Query, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.movie import MovieModel
from app.schemas.movie import Movie
from config.database import session
from app.utils.jwt_bearer import JWTBearer
from app.services.movie import MovieService

movie_router = APIRouter()

@movie_router.get("/movies", tags = ["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = session()
    results = MovieService(db).get_movies()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(results))

# parametro de ruta
@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = session()
    result = MovieService(db).get_movie_by_id(id)
    if result:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
# parametros query
@movie_router.get("/movies/", tags = ["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session()
    results = MovieService(db).get_movies_by_category(category)
    db.close()
    if results:
        return JSONResponse(status_code=200, content=jsonable_encoder(results))
    else:
        return JSONResponse(status_code=404, content={"message":"movie not found"})
    
@movie_router.post("/movies", tags = ["movies"], response_model=dict)
def create_movie(movie:Movie) -> dict:
    db = session()
    MovieService(db).create_movie(movie)
    db.close()
    return JSONResponse(status_code=201, content={"message":"Succesfully registered"})

@movie_router.put("/movies/{id}", tags=["movies"], status_code=200, response_model=dict)
def update_movie(id: int, movie:Movie) -> dict:
    db = session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"Movie not found"})      

    MovieService(db).update_movie(id, movie)
    db.close()
    return JSONResponse(status_code=200, content={"message":"Succesfully updated"}) 

@movie_router.delete("/movies/{id}", tags = ["movies"], status_code=200, response_model=dict)
def delete_movie(id:int = Path(ge=0, le=2000)) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message":"Movie not found"})
    
    MovieService(db).delete_movie(id)
    db.close()
    return JSONResponse(status_code=200, content={"message":"Succesfully deleted"})