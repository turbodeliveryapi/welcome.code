import telebot
import requests
import unicodedata

#Função para padronizar as respostas do usuário
def resposta_usuario(resposta):
    #Transforma a resposta do usuário em uma string com caracteres minusculos
    #NFD = Separa os caracteres dos acentos (á = 'a' e '´')
    resposta = resposta.lower()
    resposta = unicodedata.normalize('NFD', resposta)

    #Filtro para remover os caracteres de acentos
    resposta_normalizada = ''
    for c in resposta:
        if unicodedata.category(c) != 'Mn':
            resposta_normalizada = resposta_normalizada + c


    print (resposta_normalizada)
