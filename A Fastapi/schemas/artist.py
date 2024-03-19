from . import Base

class Artist(Base):
    ArtistId: int
    Name: str

class GetAlbum(Base):
    ArtistId: int
    Name: str
