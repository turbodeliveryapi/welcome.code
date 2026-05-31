import os
import time
import threading
import telebot
from dotenv import load_dotenv

# Importa as funções do fluxo 
from formulario import (
    iniciar_conversa,
    processar_resposta,
    processar_gestante,
    processar_tipo_pessoa,
    processar_bebe,
    obter_usuario,
    remover_usuario
)

from grupos_especiais import (
    iniciar_grupos_especiais,
    processar_quem_recebe,
    processar_locais_vacinancao_crie,
    processar_rie,
    processar_fonte_crie,
    processar_voltar_grupos_especiais
)

import scraping.scraper_pdf as scraper_pdf
import scraping.scraper_vacinas as scraper_vacinas

# Carrega o token do .env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN or not TOKEN.strip():
    print("❌ Erro: TELEGRAM_TOKEN não configurado no .env")
    exit(1)

# Inicializa o bot (com threads para não travar operações bloqueantes)
bot = telebot.TeleBot(TOKEN.strip(), threaded=True, num_threads=10)

# Palavras-chave que reiniciam o fluxo
saudacoes = ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'ajuda', 'start', 'opa', 'eae', 'eai', 'dia', 'tarde', 'noite', 'fala']

def responder_callback_seguro(call):
  #Confirma o clique no botão para o Telegram (remove o reloginho do botão)
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

# --- COMANDOS E TRATAMENTO DE MENSAGENS ---

@bot.message_handler(commands=['start', 'reiniciar'])
def comando_start(msg):
    remover_usuario(msg.chat.id)
    iniciar_conversa(bot, msg.chat.id)

@bot.message_handler(commands=['comorbidades'])
def comando_comorbidades(msg):

    iniciar_grupos_especiais(bot, msg.chat.id)

@bot.message_handler(func=lambda msg: True)
def tratar_mensagens(msg):
    if not msg.text:
        return

    texto = msg.text.lower().strip()

    # Se for uma saudação, inicia conversa
    if any(s in texto for s in saudacoes):
        iniciar_conversa(bot, msg.chat.id)
        return
    
    if 'comorbidades' in texto:
        comando_comorbidades(msg)
        return

    # Caso contrário, passa para o formulário processar
    processar_resposta(bot, msg)

# --- HANDLERS DE CALLBACK (BOTÕES INLINE) ---
    #Handlers que respondem aos cliques dos botões inline e encaminham o fluxo do formulário

    #Mostra informações sobre o bot e pergunta o nome (acionado pelo botão "Saiba Mais")
@bot.callback_query_handler(func=lambda call: call.data == "saiba_mais")
def cb_saiba_mais(call):
    responder_callback_seguro(call)
    texto = (
        "🤖 *Sobre o HealthyBot*\n\n"
        "Consulta realizada através do Site Oficial do MINISTÉRIO DA SAÚDE:\n\n"
        "✅ *Informação e cuidado na palma da sua mão*\n"
        "• Localizo vacinas por faixa etária\n"
        "• Verifico doses para gestantes\n"
        "• Mostro o que cada vacina previne\n"
        "• Envio o calendário vacinal\n\n"
        "👇 Vamos continuar? Qual é o seu nome?"
    )
    bot.send_message(call.message.chat.id, texto, parse_mode='Markdown')

#Pergunta se a consulta é para o próprio usuário ou para outra pessoa
@bot.callback_query_handler(func=lambda call: call.data in ["user", "outra_pessoa"])
def cb_tipo_pessoa(call):
    responder_callback_seguro(call)
    processar_tipo_pessoa(bot, call)

#Pergunta se é um bebê (até 2 anos) e encaminha para fluxo de meses/idade
@bot.callback_query_handler(func=lambda call: call.data.startswith(("bebe", "nao_bebe")))
def cb_bebe(call):
    responder_callback_seguro(call)
    processar_bebe(bot, call)

#Pergunta se a pessoa está gestante; define a próxima etapa conforme a resposta
@bot.callback_query_handler(func=lambda call: call.data in ["gestante", "nao_se_aplica"])
def cb_gestante(call):
    responder_callback_seguro(call)
    processar_gestante(bot, call)

    #Gera e envia o Calendário Oficial para o usuário:
    #valida sessão (faixa), envia mensagem de espera e dispara um worker em thread
    #o worker orquestra a chamada ao scraper e cuida da UX (remoção da mensagem de espera e limpeza da sessão)
@bot.callback_query_handler(func=lambda call: call.data == "mais_info")
def cb_mais_info(call):
    responder_callback_seguro(call)

    uid = call.message.chat.id
    u = obter_usuario(uid)
    faixa = u.get('faixa')

    if not faixa:
        bot.send_message(uid, "⚠️ Sessão expirada. Digite 'Oi' para reiniciar.")
        return

    msg_espera = bot.send_message(uid, "⏳ Gerando imagens do calendário oficial... Aguarde.")

    #Envia o calendário oficial em background:
    #chama scraper_pdf.enviar_paginas_como_foto(bot, uid, faixa)
    #remove a mensagem de espera, avisa quando terminar e limpa a sessão do usuário
    def _enviar_calendario_em_background():
        try:
            scraper_pdf.enviar_paginas_como_foto(bot, uid, faixa)
            bot.delete_message(uid, msg_espera.message_id)
            bot.send_message(uid, "✅ Calendário enviado! Se precisar de algo mais, digite 'Oi' 💙")
            remover_usuario(uid)
        except Exception as e:
            print(f"Erro PDF: {e}")
            bot.send_message(uid, "❌ Erro ao baixar o PDF oficial.")

    threading.Thread(target=_enviar_calendario_em_background, daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data == "quem_recebe")
def cb_quem_recebe(call):
    responder_callback_seguro(call)
    processar_quem_recebe(bot, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "locais_vacinacao_crie")
def cb_locais_vacinacao_crie(call):
    responder_callback_seguro(call)
    processar_locais_vacinancao_crie(bot, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "rie")
def cb_rie(call):
    responder_callback_seguro(call)
    processar_rie(bot, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "fonte_crie")
def cb_fonte_crie(call):
    responder_callback_seguro(call)
    processar_fonte_crie(bot, call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "voltar_grupos_especiais")
def cb_voltar_grupos_especiais(call):
    responder_callback_seguro(call)
    processar_voltar_grupos_especiais(bot, call.message.chat.id)

#  --- MENSAGEM FINAL ---

@bot.callback_query_handler(func=lambda call: call.data == "interacao_final")
def mensagem_final(call):
    responder_callback_seguro(call)
    texto = (
        "🤖 *O que mais você deseja fazer? Escolha uma das opções abaixo:*\n\n"
        "• Consultar vacinas\n\n"
        "• Consultar restrições para comorbidades\n"
        "• Consultar informações sobre vacinas especiais\n"
        "• Ver UBSs próximas a mim \n"
        "• Ver coberturas vacinais\n"
        "• Ver alternativas de vacinação domiciliar\n"
        "• Saber mais sobre o bot\n"
        "• Finalizar interação\n\n"
        "👇 Digite uma das opções mencionadas."
    )

@bot.callback_query_handler(func=lambda call: call.data == "vacinacao_domiciliar")
def cb_mais_info(call):
    responder_callback_seguro(call)

    texto = (
            "🏠Passos para solicitar atendimento domiciliar💉\n\n\n"
            "1️⃣Identificar a Unidade Básica de Saúde (UBS) mais próxima da residência do paciente.\n\n"
            "2️⃣ Um familiar deve comparecer à UBS levando:\n"
            "• Documento de identificação do paciente;\n"
            "• Cartão do SUS;\n"
            "• Comprovante de residência.\n\n"
            "3️⃣Apresentar um laudo ou relatório médico justificando a impossibilidade de locomoção.\n\n"
            "4️⃣Solicitar a inclusão do paciente no cronograma de visitas da equipe de saúde da família ou dos Agentes Comunitários de Saúde (ACS).\n\n"
            "👇 Vamos continuar? Qual é o seu nome?"
    )
    bot.send_message(call.message.chat.id, texto, parse_mode='Markdown')


# --- INICIALIZAÇÃO DO BOT ---

if __name__ == "__main__":
    # Pré-carrega o site do governo para ter cache e deixar as respostas mais rápidas
    try:
        scraper_vacinas.busca_vacinas()
        print("🟢 Cache do site carregado!")
    except Exception:
        print("🟡 Aviso: Site do governo indisponível no momento.")

    print("🚀 Bot online e aguardando mensagens...")

    while True:
        try:
            bot.polling(none_stop=True, skip_pending=True, timeout=60)
        except Exception as e:
            print(f"💥 Erro no polling: {e}")
            time.sleep(5)