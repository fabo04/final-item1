from . import Base

class User(Base):
    Id: int 
    Username: str
    Fullname: str
    Password: str
    IsAdmin :bool

class CreateUserIn(Base):
    Username: str
    Fullname: str
    Password: str

class CreateUserOut(Base):
    Id: int 
    Username: str
    Fullname: str
    Password: str
    IsAdmin :bool

class LoginUserIn(Base):
    Username: str
    Password: str

class GetUser(Base):
    Id: int 
    Username: str
    Fullname: str
    Password: str
    IsAdmin :bool