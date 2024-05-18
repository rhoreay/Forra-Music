import requests
import datetime
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#faz a requisicao de um token e define horario de vencimento
def gerarToken(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    header = {"Content_type": "application/x-www-form-urlencoded"}
    body = {"grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret}
    response = requests.post(url, headers=header, data=body)
    token = response.json()['access_token']

    #definindo tempo de vencimento ao token (55 minutos apos criacao)
    horarioToken = datetime.datetime.now()
    expiraToken = horarioToken + datetime.timedelta(minutes=55)
    vencimentoToken = expiraToken.strftime("%Y-%m-%d %H:%M:%S")

    return token, vencimentoToken


#registra as credenciais ao banco de dados
def registraCredenciais(client_id, client_secret, token, vencimentoToken):
    cursor.execute('INSERT INTO Credenciais(client_id, client_secret, token, vencimento_token) VALUES(?,?,?,?)', (client_id, client_secret, token, vencimentoToken))
    connection.commit()


#verifica e atualiza o token (se necessario). E retorna o token
def pegaToken():

    #pega a coluna de vencimento do token, converte para <datetime object> e verifica se ainda é valido
    vencimentoTokenString = cursor.execute('''SELECT vencimento_token FROM Credenciais''').fetchone()[0]
    vencimentoToken = datetime.datetime.strptime(vencimentoTokenString, '%Y-%m-%d %H:%M:%S')

    #verifica se o Token ainda é valido e o atualiza caso nao seja
    if (vencimentoToken > datetime.datetime.now()):
        token = cursor.execute('''SELECT token FROM Credenciais''').fetchone()[0]
        return token
    else:
        client_id = cursor.execute('''SELECT client_id FROM Credenciais''').fetchone()[0]
        client_secret = cursor.execute('''SELECT client_secret FROM Credenciais''').fetchone()[0]
        novoToken, vencimentoNovoToken = gerarToken(client_id, client_secret)
        cursor.execute('UPDATE Credenciais SET token = ?, vencimento_token = ? WHERE id = 1', (novoToken, vencimentoNovoToken))
        connection.commit()
        return novoToken