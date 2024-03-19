from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user
from routes.album import album
from routes.artist import artist


from sqlalchemy_utils import database_exists, create_database

app = FastAPI(
    openapi_tags=[{
        "Title": "",
        "description": "",
        "version": "0.0.1",
        "name": "",
    }]
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user, prefix='/users')
app.include_router(album, prefix='/album')
app.include_router(artist, prefix='/artist')


@app.get('/', tags=['Home App'])
@app.get('/home', tags=['Home App'])
def root():
    return 'Hola, todavía no funciona. Gracias por esperar :D'


@app.get('/test', tags=['Home App'])
def test():
    resp = {'nombre':'John', 
            'apellido': 'Doe', 
            'edad': 91}
    return resp
