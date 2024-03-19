from schemas.album import *
from models.models import AlbumDB
from methods.cnx import SessionLocal

def getAlbums():
    try:
        db = SessionLocal()
        album = db.query(AlbumDB).all()
        if album:
            db.close()
            return album
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

def getAlbumDB(AlbumId: int):
    try:
        db = SessionLocal()
        album = db.query(AlbumDB).filter(AlbumDB.AlbumId == AlbumId).first()
        if album:
            db.close()
            return album
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

def createAlbumDB(ArtistId: int, Album: CrateAlbumIn):
    try:
        db = SessionLocal()
        new_album = AlbumDB(
            Title=Album.Title,
            ArtistId=ArtistId,
            Column1=Album.Column1
        )
        db.add(new_album)
        db.commit()
        db.refresh(new_album)
        return new_album
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def updateAlbumDB(AlbumId: int, updated_album: UpdateAlbum):
    try:
        db = SessionLocal()
        album = db.query(AlbumDB).filter(AlbumDB.AlbumId == AlbumId).first()

        if album:
            album.Title = updated_album.Title
            album.ArtistId = updated_album.ArtistId
            album.Column1 = updated_album.Column1
            db.commit()
            return album
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def deleteAlbumDB(AlbumId: int):
    try:
        db = SessionLocal()
        album = db.query(AlbumDB).filter(AlbumDB.AlbumId == AlbumId).first()
        if album:
            db.delete(album)
            db.commit()
            return album  # Devuelve el álbum eliminado
        else:
            return None  # Si no se encuentra ningún álbum con ese ID, devuelve None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

                