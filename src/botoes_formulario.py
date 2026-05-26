from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Teclados inline usados pelo bot 

def saiba_mais():
    teclado = InlineKeyboardMarkup()
    teclado.add(InlineKeyboardButton("ℹ️ Saiba Mais", callback_data="saiba_mais"))
    return teclado


def tipo_pessoa():
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("👤 Para mim", callback_data="user"),
        InlineKeyboardButton("👥 Outra pessoa", callback_data="outra_pessoa")
    )
    return teclado


def gestante():
    # Pergunta se a pessoa está gestante.
    
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("🤰 Sim, gestante", callback_data="gestante"),
        InlineKeyboardButton("🚫 Não", callback_data="nao_se_aplica")
    )
    return teclado


def bebe():
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("👶 Sim, bebê", callback_data="bebe"),
        InlineKeyboardButton("🧒 Não", callback_data="nao_bebe")
    )
    return teclado


def mais_informacoes():
    teclado = InlineKeyboardMarkup()
    teclado.add(InlineKeyboardButton("📄 Ver Calendário Oficial", callback_data="mais_info"))
    return teclado

def grupos_especiais():
    teclado = InlineKeyboardMarkup(row_width=2)

    btn_quem_recebe = InlineKeyboardButton("👥 Quem pode receber?", callback_data="quem_recebe")
    btn_locais_vacinacao_crie = InlineKeyboardButton("📍 Locais de Vacinação", callback_data="locais_vacinacao_crie")
    btn_rie = InlineKeyboardButton("🏥 O que é a RIE?", callback_data="rie")
    btn_fonte_crie = InlineKeyboardButton("🔗 Fonte Oficial", callback_data="fonte_crie")
    
    teclado.add(btn_quem_recebe, btn_locais_vacinacao_crie)
    teclado.add(btn_rie, btn_fonte_crie)
    
    return teclado