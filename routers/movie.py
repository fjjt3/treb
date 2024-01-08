from models import models, schemas
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from typing import List
from fastapi import APIRouter, Query, HTTPException, Header

router =  APIRouter(tags=['Movies'],
                    prefix="/movie")



@router.get('/', response_model=List[schemas.Movie]) 
def get_movies(db: Session = Depends(get_db), 
            limit: int = Query(10, description="Número de películas por página"), 
            offset: int = Query(5, description="Número de películas a omitir")):
    movies = db.query(models.Movie).order_by(models.Movie.title).offset(offset).limit(limit).all() 
    return movies

@router.get('/{title}', response_model=schemas.Movie)
def get_movie_by_title(title: str, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.title == title).first()
    return movie

@router.post('/', response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie



"""@router.delete('/{imdbID}')
def delete_movie(imdbID: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization != "12345":
        raise HTTPException(status_code=403, detail="Unauthorized")

    movie = db.query(models.Movie).filter(models.Movie.imdbID == imdbID).first()
    if movie:
        db.delete(movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Movie not found") """

@router.delete('/{imdbID}')
def delete_movie(imdbID: str, authorization: str = Header(None), db: Session = Depends(get_db)):
    expected_authorization = "12345"  # Valor esperado del encabezado de autorización

    if authorization != expected_authorization:
        raise HTTPException(status_code=403, detail="La autorización es inválida o faltante")

    movie = db.query(models.Movie).filter(models.Movie.imdbID == imdbID).first()
    if movie:
        db.delete(movie)
        db.commit()
        return {"message": "Película eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Película no encontrada")