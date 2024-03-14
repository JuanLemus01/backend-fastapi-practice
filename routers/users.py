from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/users',tags=['Users'])

#User Entity
class User(BaseModel):
    id: int
    name: str
    lastname: str
    age : int

users_test = [User(id=1,name='Juan',lastname='Lemus',age=23),
              User(id=2,name='Andres',lastname='Med',age=22),
              User(id=3,name='Pepe',lastname='rats',age=14)]

@router.get('/',status_code=200)
async def users_list():
    return users_test


@router.get('/{id}',status_code=200)
async def user_by_id(id:int):
    return search_user(id)


@router.post('/',response_model=User, status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail='El usuario ya existe')
    else:
        return users_test.append(user)

def search_user(id:int):
    user_filter = list(filter(lambda user : user.id == id,users_test ))
    try:  
        return user_filter[0]
    except:
        return {'detail':'No se ha encontrado ese usuario'}
   