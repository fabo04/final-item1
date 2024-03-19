from . import Base

class Album(Base):
    AlbumId: int
    Title: str
    ArtistId: int

class CrateAlbumIn(Base):
    Title: str
    ArtistId: int
    Column1: str

class CrateAlbumOut(Base):
    AlbumId: str
    Title: str
    ArtistId: int
    Column1: str

class CreateAlbum(Base): #borrar?
    Title: str
    ArtistId: int
    Column1: str

class GetAlbum(Base):
    AlbumId: int
    Title: str
    ArtistId: int
    
class UpdateAlbum(Base):
    Title: str
    ArtistId: int
    Column1: str
