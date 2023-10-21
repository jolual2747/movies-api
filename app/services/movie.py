from app.models.movie import MovieModel
from app.schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        results = self.db.query(MovieModel).all()
        return results
    
    def get_movie_by_id(self, id:id):
        results = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return results
    
    def get_movies_by_category(self, category:str):
        results = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return results
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id:int, data:Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()

    def delete_movie(self, id:int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(movie)
        self.db.commit()
