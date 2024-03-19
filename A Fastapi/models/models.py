from sqlalchemy import String, Integer, Boolean, BLOB
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class UserDB(Base):
    __tablename__ = "Users"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, unique=True, index=True)
    Fullname = Column(String)
    Password = Column(String)
    IsAdmin = Column(Boolean, default=False)

class ArtistDB(Base):
    __tablename__ = "Artist"
    ArtistId = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100))
    Album = relationship("AlbumDB", backref="Artist", lazy=True)

class AlbumDB(Base):
    __tablename__ = "Album"
    AlbumId = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String(100))
    ArtistId = Column(Integer, ForeignKey("Artist.ArtistId"))
    Column1 = Column(String(100))