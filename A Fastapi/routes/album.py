from fastapi import APIRouter
from fastapi import HTTPException
from schemas.album import *
from methods.albumdb import *
from typing import List

album = APIRouter()

@album.get('', response_model=List[Album], tags=['Album'])
async def get_all_album():
    try:
        albums = getAlbums()  
        if albums:
            return albums
        raise HTTPException(status_code=404, detail='No albums found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting albums: {e}")

@album.get('/{AlbumId}',response_model=Album , tags=['Album'])
async def get_album(AlbumId: int):
    try:
        album = getAlbumDB(AlbumId=AlbumId)
        if album:
            return album
        raise HTTPException(status_code=404, detail=f'Album: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting album {id}: {e}")

@album.post('/',response_model=CreateAlbum , tags=['Album'])
async def create_album(album: CreateAlbum):
    try:
        new_album = createAlbumDB(album.ArtistId, album)
        response = CreateAlbum(
            AlbumId=new_album.AlbumId,
            Title=new_album.Title,
            ArtistId=new_album.ArtistId,
            Column1=new_album.Column1
        )
        return response
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: album creation failed: {e}")





@album.put('/{AlbumId}', response_model=UpdateAlbum, tags=['Album'])
async def update_album(AlbumId: int, updated_album: UpdateAlbum):
    try:
        updatedAlbum = updateAlbumDB(AlbumId, updated_album)
        if updatedAlbum:
            return updated_album  # Devuelve el objeto actualizado
        raise HTTPException(status_code=404, detail=f'Album: {AlbumId} not found')
    except Exception as e:
        raise HTTPException(status_code=501, detail=f"Update Failed for album ID: {AlbumId}, Error {e}")










@album.delete('/{AlbumId}', response_model=Album, tags=['Album'])
async def delete_album(AlbumId: int):
    try:
        deletedAlbum = deleteAlbumDB(AlbumId=AlbumId)
        if deletedAlbum is not None:  
            return deletedAlbum
        else:
            raise HTTPException(status_code=404, detail=f'Album with ID {AlbumId} not found')  
    except HTTPException as http_error:  # Maneja específicamente las excepciones HTTP
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")  

