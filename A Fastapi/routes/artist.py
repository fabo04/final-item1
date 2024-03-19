from fastapi import APIRouter
from fastapi import HTTPException
from schemas import *
from methods.artistdb import *
from fastapi.responses import JSONResponse
from typing import List

artist = APIRouter()

@artist.get('', response_model=List[Artist], tags=['Artist'])
async def get_all_artists():
    try:
        artists = getArtists()
        if artists:
            return artists
        raise HTTPException(status_code=404, detail=f'Artists: not found')
    except Exception as e:
        raise HTTPException(status_code=503,detail=f"Error getting artists: {e}")
    
@artist.get('/{ArtistId}',response_model=Artist , tags=['Artist'])
async def get_artist(ArtistId: int):
    try:
        artist = getArtistDB(ArtistId=ArtistId)
        if artist:
            return artist
        raise HTTPException(status_code=404, detail=f'Artist: {id} not found')
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error getting artist {id}: {e}")

