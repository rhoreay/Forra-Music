from func.registrar import registrarArtista, registrarAlbum, registrarMusica, registraTodasMusicas
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
                        artistaURL = input('Qual a URL do perfil desse artista: ')
                        artista_spotifyID = pegaID(artistaURL)
                        registrarArtista(artista_spotifyID)
                        
                case '2':#registrar novo album
                        albumURL = input('Qual a URL do album: ')
                        album_spotifyID = pegaID(albumURL)
                        registrarAlbum(album_spotifyID)
                case '3':#registrar musica
                        musicaURL = input('Qual a URL da musica: ')
                        musica_spotifyID = pegaID(musicaURL)
                        registrarMusica(musica_spotifyID)
                case '4':#registrar todas musicas de um album
                        albumURL = input('Qual a URL do album: ')
                        album_spotifyID = pegaID(albumURL)
                        registraTodasMusicas(album_spotifyID)
                case '5':
                        os.system('cls')
                case '6':
                        break
                case _:
                        print('COMANDO INVALIDO')