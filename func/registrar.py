from func.pegaToken import pegaToken
import sqlite3
import requests

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#registra novo artista
def registrarArtista(nomeArtista, artista_spotifyID):
    #verifica se o artista ja esta cadastrado
    if cursor.execute("SELECT * FROM ARTISTAS WHERE artista_spotify_id = ?", (artista_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Artistas (nome, artista_spotify_id) VALUES (?, ?)", (nomeArtista, artista_spotifyID))
        connection.commit()

#registra novo album
def registrarAlbum(tituloAlbum, artistas, album_spotifyID):
    #verifica se o album ja esta cadastrado e o cadastra se nao estiver
    if cursor.execute("SELECT * FROM ALBUMS WHERE album_spotify_id = ?", (album_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Albums (titulo, album_spotify_id) VALUES (?, ?)", (tituloAlbum, album_spotifyID))
        connection.commit()

    #pega o albumID do album 
    albumId = cursor.execute("SELECT album_id FROM Albums WHERE album_spotify_id = ?", (album_spotifyID,)).fetchone()[0]

    #registra os artistas do album e relaciona na tabela artistas_albums
    for artista in artistas:
        artista_spotifyID = artista['id']
        nomeArtista =  artista['name']
        registrarArtista(nomeArtista, artista_spotifyID)
        artistaId = cursor.execute("SELECT artista_id FROM Artistas WHERE artista_spotify_id = ?", (artista_spotifyID,)).fetchone()[0]
        #verifica se ja existe a relacao na tabela artistas_albums
        if cursor.execute("SELECT * FROM artistas_albums WHERE artista_id = ? AND album_id = ?", (artistaId, albumId)).fetchone() == None:
            cursor.execute("INSERT INTO Artistas_Albums (album_id, artista_id) VALUES (?, ?)", (albumId, artistaId))
    
    connection.commit()

def registrarMusica(musica_spotifyID):
    #request para pegar o nome, album e artistas da musica
    url = f'https://api.spotify.com/v1/tracks/{musica_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    
    tituloMusica = response.json()['name']
    artistas = response.json()['artists']
    album_spotifyID = response.json()['album']['id']
    
    registrarAlbum(album_spotifyID)
    albumId = cursor.execute("SELECT album_id FROM Albums WHERE album_spotify_id =?", (album_spotifyID,)).fetchone()[0]
    
    #verifica se a musica ja esta registrada
    if cursor.execute("SELECT * FROM Musicas WHERE musica_spotify_id = ?", (musica_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Musicas (titulo, musica_spotify_id, album_id) VALUES (?, ?, ?)", (tituloMusica, musica_spotifyID, albumId))

    for artista in artistas:
        artista_spotifyID = artista['id']
        registrarArtista(artista_spotifyID)
        
        artistaId = cursor.execute("SELECT artista_id FROM Artistas WHERE artista_spotify_id =?", (artista_spotifyID,)).fetchone()[0]
        musicaId = cursor.execute("SELECT musica_id FROM Musicas WHERE musica_spotify_id = ?", (musica_spotifyID,)).fetchone()[0]
        #verifica se ja existe a relacao na tabela artistas_musicas
        if cursor.execute("SELECT * FROM artistas_musicas WHERE musica_id = ? AND artista_id = ?", (musicaId, artistaId)).fetchone() == None:
            cursor.execute("INSERT INTO artistas_musicas (musica_id, artista_id) VALUES (?,?)", (musicaId, artistaId))

    connection.commit()

def registraTodasMusicasAlbum(album_spotifyID):
    #request para pegar as musicas do album
    url = f'https://api.spotify.com/v1/albums/{album_spotifyID}'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    musicas = response.json()['tracks']['items']

    for musica in musicas:
        musica_spotifyID = musica['id']
        registrarMusica(musica_spotifyID)

def registraMusicasPlaylist(playlist_spotify_id):
    #request para pegar as musicas da playlist
    url = f'https://api.spotify.com/v1/playlists/{playlist_spotify_id}?fields=tracks.items%28track%28id%2C+name%29%29'
    header = {"Authorization": f"Bearer {pegaToken()}"}
    response = requests.get(url, headers=header)
    musicas = response.json()['tracks']['items']
    for musica in musicas:
        musica_spotifyID = musica['track']['id']
        registrarMusica(musica_spotifyID)