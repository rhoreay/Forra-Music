import re

#extrai o ID de musicas, albums e artistas pela URL usando RegEx
def pegaID(url):
        id = re.findall(r'/(artist|track|album|playlist)/([a-zA-Z0-9]+)\?', url)[0][1]
        return id