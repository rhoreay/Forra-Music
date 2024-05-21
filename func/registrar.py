from func.pegaToken import pegaToken
import sqlite3
import requests

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#registra novo artista
def registrarArtista(artistaInfo):
    nomeArtista = artistaInfo['name']
    artista_spotifyID = artistaInfo['id']
    #verifica se o artista ja esta cadastrado
    if cursor.execute("SELECT * FROM ARTISTAS WHERE artista_spotify_id = ?", (artista_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Artistas (nome, artista_spotify_id) VALUES (?, ?)", (nomeArtista, artista_spotifyID))
        connection.commit()

#registra novo album
def registrarAlbum(albumInfo):
    tituloAlbum = albumInfo['name']
    artistas = albumInfo['artists']
    album_spotifyID = albumInfo['id']
    #verifica se o album ja esta cadastrado e o cadastra se nao estiver
    if cursor.execute("SELECT * FROM ALBUMS WHERE album_spotify_id = ?", (album_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Albums (titulo, album_spotify_id) VALUES (?, ?)", (tituloAlbum, album_spotifyID))
        connection.commit()

    #pega o albumID do album 
    albumId = cursor.execute("SELECT album_id FROM Albums WHERE album_spotify_id = ?", (album_spotifyID,)).fetchone()[0]

    #registra os artistas do album e relaciona na tabela artistas_albums
    for artista in artistas:
        registrarArtista(artista)
        artista_spotifyID = artista['id']
        artistaId = cursor.execute("SELECT artista_id FROM Artistas WHERE artista_spotify_id = ?", (artista_spotifyID,)).fetchone()[0]
        #verifica se ja existe a relacao na tabela artistas_albums
        if cursor.execute("SELECT * FROM artistas_albums WHERE artista_id = ? AND album_id = ?", (artistaId, albumId)).fetchone() == None:
            cursor.execute("INSERT INTO Artistas_Albums (album_id, artista_id) VALUES (?, ?)", (albumId, artistaId))
    
    connection.commit()

def registrarMusica(musicaInfo):
    tituloMusica = musicaInfo['name']
    artistas = musicaInfo['artists']
    musica_spotifyID = musicaInfo['id']
    albumInfo = musicaInfo['album']
    
    #primeiramente registra o album qual a musica pertence
    registrarAlbum(albumInfo)
    album_spotifyID = musicaInfo['album']['id']
    albumId = cursor.execute("SELECT album_id FROM Albums WHERE album_spotify_id =?", (album_spotifyID,)).fetchone()[0]
    
    #verifica se a musica ja esta registrada
    if cursor.execute("SELECT * FROM Musicas WHERE musica_spotify_id = ?", (musica_spotifyID,)).fetchone() == None:
        cursor.execute("INSERT INTO Musicas (titulo, musica_spotify_id, album_id) VALUES (?, ?, ?)", (tituloMusica, musica_spotifyID, albumId))

    for artista in artistas:
        registrarArtista(artista)
        artista_spotifyID = artista['id']
        
        artistaId = cursor.execute("SELECT artista_id FROM Artistas WHERE artista_spotify_id =?", (artista_spotifyID,)).fetchone()[0]
        musicaId = cursor.execute("SELECT musica_id FROM Musicas WHERE musica_spotify_id = ?", (musica_spotifyID,)).fetchone()[0]
        #verifica se ja existe a relacao na tabela artistas_musicas
        if cursor.execute("SELECT * FROM artistas_musicas WHERE musica_id = ? AND artista_id = ?", (musicaId, artistaId)).fetchone() == None:
            cursor.execute("INSERT INTO artistas_musicas (musica_id, artista_id) VALUES (?,?)", (musicaId, artistaId))

    connection.commit()
