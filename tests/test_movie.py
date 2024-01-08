import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from routers import movie

# Crea una función para inicializar la base de datos en memoria y cargar datos de prueba
@pytest.fixture(scope="module")
def db():
    engine = create_engine('sqlite:///:test_db:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    return engine

def test_create_movie(db):
    client = TestClient(movie)
    response = client.post("/movie/", json={"title": "Test Movie"})
    assert response.status_code == 200 

def test_get_movies(db):
    client = TestClient(movie)
    response = client.get("/movie/")
    assert response.status_code == 200

def test_get_movie_by_title(db):
    client = TestClient(movie)
    response = client.get("/movie/{Test Movie}")
    assert response.status_code == 200

def test_delete_movie(db):
    client = TestClient(movie)
    response = client.delete("/movie/{Test Movie}", headers={"authorization": "12345"})
    assert response.status_code == 200