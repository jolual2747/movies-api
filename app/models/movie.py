from pydantic import BaseModel, Field
from typing import Optional
from config.database import base
from sqlalchemy import Column, Integer, String, Float

class Movie(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int  = Field(le = 2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    # example of the schema

    model_config = {
        "json_schema_extra": {
            "examples" : [
                {
                    "id" : 3,
                    "title" : "My Movie",
                    "overview" : "This is the overview of the movie",
                    "year" : 2021,
                    "rating" : 8.5,
                    "category" : "Accion"
                }
            ]
        }
    }

class MovieModel(base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)