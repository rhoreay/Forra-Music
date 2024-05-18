from func.pegaToken import pegaToken
import sqlite3
import requests

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


#registra novo artista
def registrarArtista(artista_spotifyID):
    #request para pegar o nome do artista
    url = f'https://api.spotify.com/v1/artists/{artista_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    nome = response.json()['name']

    #verifica se o artista ja esta cadastrado
    if cursor.execute("""SELECT * FROM ARTISTAS WHERE artista_spotify_id = ?""", (artista_spotifyID,)).fetchone() == None:
        cursor.execute("""INSERT INTO Artistas (nome, artista_spotify_id) VALUES (?, ?)""", (nome, artista_spotifyID))
        connection.commit()

