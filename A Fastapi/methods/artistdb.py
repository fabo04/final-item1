from schemas.artist import *
from models.models import ArtistDB
from methods.cnx import SessionLocal

def getArtists():
    try:
        db = SessionLocal()
        artist = db.query(ArtistDB).all()
        if artist:
            db.close()
            return artist
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

def getArtistDB(ArtistId: int):
    try:
        db = SessionLocal()
        artist = db.query(ArtistDB).filter(ArtistDB.ArtistId == ArtistId).first()
        if artist:
            db.close()
            return artist
        return None
    except Exception as e:
        raise e
    finally:
        db.close()