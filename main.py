import sqlite3
import requests
from fastapi import FastAPI
from routers import movie

app = FastAPI()

app.include_router(movie.router)

@app.on_event("startup")
async def startup_event():
    conn = sqlite3.connect('movies_bret.db')
    c = conn.cursor()

    # Comprueba si la tabla existe
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='MOVIES' ''')

    # Si la tabla no existe, la crea e inserta los datos
    if c.fetchone()[0] == 0:
        c.execute('''CREATE TABLE MOVIES
                    (title text, year text, imdbID text)''')
        for page in range(1, 11):  # Hacer 10 llamadas a la API
            response = requests.get(f'http://www.omdbapi.com/?s=movie&apikey=34600ae8&page={page}')
            data = response.json()
            for movie in data['Search']:
                c.execute("INSERT INTO MOVIES VALUES (?, ?, ?)",
                        (movie['Title'], movie['Year'], movie['imdbID']))

        # Guarda (commit) los cambios
        conn.commit()

    # Cierra la conexión
    conn.close()

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutdown event")