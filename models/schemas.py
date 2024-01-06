from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    title: str
    year: str
    imdbID: str
    

class MovieCreate(BaseModel):
    title: str
    year: str
    imdbID: str
    