from func.registrar import registrarArtista, registrarAlbum, registrarMusica, registraTodasMusicasAlbum, registraMusicasPlaylist
from func.fetchs import fetchArtista, fetchAlbum
from func.pegaToken import gerarToken, registraCredenciais
from func.criaDatabase import createDatabase
from func.pegaID import pegaID
import sqlite3 
import os 
from time import sleep

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("""PRAGMA foreign_keys = ON""") 

createDatabase()
interface = open('interface.txt', 'r').read()
primeiroAcesso = open('primeiroAcesso.txt', 'r').read()


while True:
        sleep(0.35)
        #verifica se existe algum token ja registrado
        if cursor.execute('''SELECT token FROM Credenciais''').fetchone() != None:
                print(interface)

        #caso nao tenha, o sistema presume que seja o primeiro acesso
        else:                
                print(primeiroAcesso)
                client_id = input('Digite seu client_id: ')
                client_secret = input('Digite seu client_secret: ')
                token, vencimentoToken = gerarToken(client_id, client_secret)
                registraCredenciais(client_id, client_secret, token, vencimentoToken)
                os.system('cls')
                print(interface)


        comando = input('>')
        match comando:
                case '1':#registrar novo artista
                        artista_spotifyID = pegaID(input('Qual a URL do perfil desse artista: '))
                        nomeArtista = fetchArtista(artista_spotifyID)['name']
                        registrarArtista(nomeArtista, artista_spotifyID)                       
                case '2':#registrar novo album
                        album_spotifyID = pegaID(input('Qual a URL do album: '))
                        albumInfo = fetchAlbum(album_spotifyID)
                        tituloAlbum, artistas = albumInfo['name'], albumInfo['artists']
                        registrarAlbum(tituloAlbum, artistas, album_spotifyID)
                case '3':#registrar musica
                        musicaURL = input('Qual a URL da musica: ')
                        musica_spotifyID = pegaID(musicaURL)
                        registrarMusica(musica_spotifyID)
                case '4':#registrar todas musicas de um album
                        albumURL = input('Qual a URL do album: ')
                        album_spotifyID = pegaID(albumURL)
                        registraTodasMusicasAlbum(album_spotifyID)
                case '5':#registra todas as musicas de uma playlist
                        playlistURL = input('Qual a URL da playlist: ')
                        playlist_spotifyID = pegaID(playlistURL)
                        registraMusicasPlaylist(playlist_spotifyID)
                case '6':
                        os.system('cls')
                case '7':
                        break
                case _:
                        print('COMANDO INVALIDO')