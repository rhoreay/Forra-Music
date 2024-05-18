# Forra-Music
Projeto em Python que utitliza a API do spotify para registrar nome de artistas, albums e músicas. E os relaciona em um banco de dados SQLite3

## Ferramentas 
- Banco de dados SQLITE
- Código em Python
- API do Spotify

## Estrutura banco de dados
- Musicas (musica_id, titulo, musica_spotify_id, album_id)
- Albums (album_id, titulo, album_spotify_id)
- Artistas (artista_id, nome, artista_spotify_id)
- Artistas_Album (artista_id, album_id)
- Artistas_Musicas (artista_id, musica_id)
- Credenciais (id, client_id, client_secret, token, vencimento_token)

## Como usar:
Será necessario que voce tenha uma conta no dashboard de desenvolvedor do spotify (https://developer.spotify.com/), para que tenha um client_id e um client_secret. Dessa forma, da primeira vez que executar 'index.py' ele vai solicitar essas credenciais e guardar na tabela 'Credenciais'.

## Token:
O token disponibilizado pelo spotify tem a vida util de uma hora. Dessa forma, quando um token é solicitado e armazenado na tabela 'Credenciais', junto a ele é guardado o horario em que ele deixará de funcionar. Assim, toda vez que precisar ser feito um request na API, ele consultará a coluna 'vencimento_Token' para saber se será necessário emitir um novo ou não.
