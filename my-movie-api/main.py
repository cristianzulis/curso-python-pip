from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Example My API FASTAPI"
app.version = "0.0.1"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Accion"
                }
            ]
        }
    }

movies = [
    {
        "id":1,
        "title":"Avatar",
        "overview": "En un exuberante planeta etc",
        "year": "2009",
        "rating": 7.8,
        "category":"Accion"
    },
    {
        "id":2,
        "title":"Avatar",
        "overview": "En un exuberante planeta etc",
        "year": "2009",
        "rating": 7.8,
        "category":"Accion"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hola mundo</h1>')

@app.get('/movies', tags=['movies'], status_code=200)
def get_movies():
    return JSONResponse(status_code=200, content = movies)

#ge = mayor igual
#le = menor igual
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content = item)

    # result = next((item for item in movies if item["id"] == id), [])
    # return result
    return JSONResponse(status_code=404, content = [])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category:str = Query(min_length=5, max_length=15)):
    data = [item for item in movies if item['category']==category]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie:Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"Se registro"})

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int, movie:Movie):
    for item in movies:
        if item["id"] == id:
            item['title']= movie.title
            item['overview']= movie.overview
            item['year']= movie.year
            item['rating']= movie.rating
            item['category']= movie.category
            return JSONResponse(content={"message":"Se modifico"})

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se elimino"})