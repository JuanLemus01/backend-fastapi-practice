from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from routers import users, jwt_auth_users

#Start the server = uvicorn main:app --reload

app = FastAPI()
app.title = 'My first Python api'

#Routers 
app.include_router(users.router)
app.include_router(jwt_auth_users.router)

movies_list = [
    {
        "id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
    },
    {
        "id": 2,
		"title": "Meteoro",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2010",
		"rating": 7.8,
		"category": "Acción"
    },
    {
        "id": 3,
		"title": "Gran Turismo",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2023",
		"rating": 7.8,
		"category": "Acción"
    }
]

@app.get('/')
def message():
    return HTMLResponse("<h1>Hello world</h1>")

#lista de peliculas
@app.get('/movies',tags=['Movies'])
def get_movies():
    return movies_list


def filter_gen(id,par_movie):
    return list(filter(lambda movie : movie[par_movie] == id, movies_list)) 

#lista de peliculas por id
@app.get('/movie/',tags=['Movie By ID'])
async def get_movies_by_id(id:int):
    movie1 = filter_gen(id,'id')
    movie = [movie for movie in movies_list if movie['id'] == id]
    try: return movie[0]
    except: raise HTTPException(404, detail='No se ha encontrado esa pelicula')