from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from sqlalchemy_utils import create_database, database_exists
from config import STRCNX
from models import Base

# Crear el motor de base de datos
engine = create_engine(STRCNX)

# Pimer inicio de la Aplicacion debo saber si la base de datos esta creada o no
#if not database_exists(engine.url):
    #create_database(engine.url)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)