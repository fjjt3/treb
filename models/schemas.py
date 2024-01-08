from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    year: str
    imdbID: str
    

class MovieCreate(BaseModel):
    title: str
    year: str
    imdbID: str
    