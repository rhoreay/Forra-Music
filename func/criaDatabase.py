import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def createDatabase():
    cursor.execute("""PRAGMA foreign_keys = ON""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Artistas 
        (artista_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome VARCHAR(255) NOT NULL,
        artista_spotify_id TEXT)""")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_artista_id ON artistas(artista_id)")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_spotify_artista_id ON artistas(artista_spotify_id)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Albums (
        album_id INTEGER PRIMARY KEY,
        titulo TEXT,
        album_spotify_id TEXT)""")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_album_id ON albums(album_id)")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_spotify_album_id ON albums(album_spotify_id)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Musicas(
        musica_id INTEGER PRIMARY KEY,
        titulo TEXT,
        musica_spotify_id TEXT,
        album_id INTEGER,
        FOREIGN KEY (album_id) REFERENCES Albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE)""")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_musica_id ON musicas(musica_id)")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_musica_spotify_id ON musicas(musica_spotify_id)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Artistas_Musicas(
        musica_id INTEGER,
        artista_id INTEGER,
        FOREIGN KEY (artista_id) REFERENCES artistas(artista_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (musica_id) REFERENCES musicas(musica_id) ON DELETE CASCADE ON UPDATE CASCADE)""")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_artistaID_musica ON artistas_musicas(artista_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_musicaID_artista ON artistas_musicas(musica_id)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Artistas_Albums(
        album_id INTEGER,
        artista_id INTEGER,
        FOREIGN KEY (artista_id) REFERENCES artistas(artista_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (album_id) REFERENCES albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE)""")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_albumID_artista ON artistas_albums(album_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_artistaID_album ON artistas_albums(artista_id)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Credenciais(
        id INTEGER PRIMARY KEY,
        client_id TEXT NOT NULL,
        client_secret TEXT NOT NULL,
        token TEXT NOT NULL,
        vencimento_token TEXT NOT NULL)""")
    