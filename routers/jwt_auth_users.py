from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = 'd559e72f69a93c13978aa0fcdff19857201dfc21b5ba96ff22a99954a484ca5d'

crypt = CryptContext(schemes=['bcrypt'])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password:str

users_db = {
    'Juan01':{
       'username': 'Juan01',
       'full_name': 'Juan Lemus',
       'email': 'lemusds@dhasd.com',
        'disabled': False,
        'password':'$2a$12$3dqq9ykAkR0GKqQd97ooxe3opRyjGQo8nXV1myZhp42ZwLrBbw6fW'
    },
    'Maria01':{
       'username': 'Maria01',
       'full_name': 'Juan Lemus',
       'email': 'lemusds@dhasd.com',
        'disabled': True,
        'password':'$2a$12$P4SzhPVJ8N6TzDyWvkU6/ulJzYXRXMd75Typ4gZBPNGbyYYUSm/Ru'
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str = Depends(oauth2)):

    exception_auth = HTTPException(status_code=401, detail='Credenciales de autenticacion invalidas',headers={'WWW-Authenticate':'Bearer'}) 
    
    try:
        username = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]).get('sub')
        if username is None:
            raise exception_auth
        
    except JWTError:
        raise exception_auth
    
    return search_user(username)
        

async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail='Usuario inactivo')
    return user

@router.post('/login')
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail='El usuario no es correcto')
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail='La contraseña no es correcta')
    
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION)

    access_token = {'sub':user.username,'exp':expire}
    return {'acceso_token':jwt.encode(access_token,SECRET_KEY,algorithm= ALGORITHM ), 'token_type':'bearer'}

@router.get('/user/me')
async def me(user:User = Depends(current_user)):
    return user
