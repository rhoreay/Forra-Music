from func.pegaToken import pegaToken
import sqlite3
import requests

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#pega info de artista 
def fetchArtista(artista_spotifyID):
    url = f'https://api.spotify.com/v1/artists/{artista_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    return response.json()

#pega info de album
def fetchAlbum(album_spotifyID):
    url = f'https://api.spotify.com/v1/albums/{album_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    return response.json()