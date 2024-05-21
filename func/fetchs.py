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

def fetchMusica(musica_spotifyID):
    #request para pegar o nome, album e artistas da musica
    url = f'https://api.spotify.com/v1/tracks/{musica_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    return response.json()    

def fetchPlaylist(playlist_spotifyID):
    #request para pegar as musicas da playlist
    url = f'https://api.spotify.com/v1/playlists/{playlist_spotifyID}?fields=tracks.items%28track%28name%2Cid%2Calbum%28name%2Cid%29%29%29'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    return response.json()