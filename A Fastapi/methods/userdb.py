from sqlalchemy.exc import SQLAlchemyError
import logging
from schemas.user import *
from models.models import UserDB
from methods.cnx import SessionLocal

logger = logging.getLogger(__name__)

def getUsers():
    try:
        db = SessionLocal()
        users = db.query(UserDB).all()
        return users
    except SQLAlchemyError as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise
    finally:
        db.close()

def getUserDB(Username: str):
    try:
        db = SessionLocal()
        user = db.query(UserDB).filter(UserDB.Username == Username).first()
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user with Id {Username}: {str(e)}")
        raise
    finally:
        db.close()
    
def Userlogin(Username: str, Password: str):
    try:
        db = SessionLocal()
        user = db.query(UserDB).filter(UserDB.Username == Username, UserDB.Password == Password).first()
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error logging in user {Username}: {str(e)}")
        raise
    finally:
        db.close()
    
def createUserDB(user: CreateUserIn):
    try:
        db = SessionLocal()
        new_user = UserDB(
            Username=user.Username,
            Fullname=user.Fullname, 
            Password=user.Password,
)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating user {user.Username}: {str(e)}")
        raise
    finally:
        db.close()
