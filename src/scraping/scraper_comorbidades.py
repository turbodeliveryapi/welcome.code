import requests
from bs4 import BeautifulSoup


def buscar_info():

    try: 

        pagina = requests.get(
            'https://www.gov.br/saude/pt-br/vacinacao/grupos-especiais'
        )

        if pagina.status_code != 200:
            return "Erro ao acessar o site"

        dados_pagina = BeautifulSoup(pagina.text, 'html.parser')

        secao = dados_pagina.find(
            'div',
            class_='cover-richtext-tile tile-content'
        )

        if secao:
            paragrafos = secao.find_all('p')

            texto_comorbidades = []

            for texto in paragrafos:
                texto_limpo = " ".join(texto.text.split())
                texto_comorbidades.append(texto_limpo)

            return texto_comorbidades
            
        if not secao:
            return "Seção não encontrada"
        
    except Exception as e:
        return f"Erro: {e}"
