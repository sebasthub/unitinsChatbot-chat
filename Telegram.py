
import requests
import time
import json
import os
import requests

class TelegramBot:
    def __init__(self):
        iTOKEN  = '5639693288:AAF6UjJDexpXeBnS5mCZma04FlqBbWXZKPw'
        self.iURL = f'https://api.telegram.org/bot{iTOKEN}/'

    def Iniciar(self):
        iUPDATE_ID = None
        while True:
            iATUALIZACAO = self.ler_novas_mensagens(iUPDATE_ID)
            IDADOS = iATUALIZACAO["result"]
            if IDADOS:
                for dado in IDADOS:
                    iUPDATE_ID = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    primeira_mensagem = int(dado["message"]["message_id"]) == 1
                    resposta = self.gerar_respostas(mensagem, primeira_mensagem)
                    self.responder(resposta, chat_id)

    def ler_novas_mensagens(self, iUPDATE_ID):
        iLINK_REQ = f'{self.iURL}getUpdates?timeout=5'
        if iUPDATE_ID:
            iLINK_REQ = f'{iLINK_REQ}&offset={iUPDATE_ID + 1}'
        iRESULT = requests.get(iLINK_REQ)
        return json.loads(iRESULT.content)

    def gerar_respostas(self, mensagem, primeira_mensagem):
        print('mensagem do cliente: ' + str(mensagem))
        if primeira_mensagem == True or mensagem.lower() in ('reinicio', '/start'):
            return f'''Olá seja bem vindo ao chatbot digite seu cpf para ver os grupos que faz parte'''
        else:
            try:
                print(mensagem)
                request = requests.get(f"http://127.0.0.1:8000/grupos/{mensagem}")
                obj = json.loads(request.content)
                strg = "os grupos são: "
                for grupo in obj['grupos']:
                    strg = strg + f"\n{grupo['materia']} - {grupo['link']} " 
                return strg + '\ncaso precise dos grupos de outro cpf digite abaixo'#f'''os grupos são f{obj['grupos'] }'''
            except:
                return f"não achei nada verifique se seu cpf esta correto"

    def responder(self, resposta, chat_id):
        iLINK_REQ = f'{self.iURL}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(iLINK_REQ)
        print("respondi: " + str(resposta))


bot = TelegramBot()
bot.Iniciar() 

