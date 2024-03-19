from fastapi import APIRouter
from fastapi import HTTPException
from schemas import *
from methods.userdb import *
from fastapi.responses import JSONResponse
from typing import List

user = APIRouter()

@user.get('', response_model=List[User], tags=['Users'])
async def get_all_users():
    try:
        users = getUsers()
        if users:
            return users
        raise HTTPException(status_code=404, detail=f'Users: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting users: {e}")
    
@user.get('/{Username}', response_model=User, tags=['Users'])
async def get_user(Username: str):
    try:
        user = getUserDB(Username=Username)
        if user:
            return user
        raise HTTPException(status_code=404, detail=f'User: {Username} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting user {Username}: {e}")

@user.post('', response_model=CreateUserOut, tags=['Users'])
async def create_user(user: CreateUserIn):
    try:
        new_user = createUserDB(user=user)
        return new_user
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: User creation failed: {e}")

@user.post('/login', response_model=CreateUserOut, tags=['Users'])
async def create_user(user: LoginUserIn):
    try:
        new_user = Userlogin(Username=user.Username, Password=user.Password)
        if new_user:
            return new_user
        return JSONResponse(content={"mensaje":"user not foud"},status_code=404)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: User creation failed: {e}")
    