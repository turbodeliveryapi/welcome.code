import telebot
import botoes_formulario


def iniciar_grupos_especiais(bot, user_id):
    texto = (
        '💉*Vacinas para grupos especiais:*\n\n'

        '➡️ A vacinação de pessoas com condições clínicas específicas é essencial não apenas para protegê-las contra doenças evitáveis, mas também para garantir mais qualidade de vida, bem-estar e inclusão social.\n\n'

        '➡️ Para ampliar o acesso a essas vacinas, o SUS conta com a Rede de Imunobiológicos para Pessoas com Situações Especiais (RIE), responsável pelo atendimento de grupos especiais em saúde.\n\n'

        '📌 *Consulte mais informações navegando pelos botões abaixo:*\n\n'
    )

    bot.send_message(
        user_id,
        texto,
        parse_mode='Markdown',
        reply_markup=botoes_formulario.grupos_especiais()
    )

def processar_quem_recebe(bot, user_id):
    texto = (
        '✅ *Grupos que podem ter acesso às vacinas especiais:*\n\n'

        '• Pessoas portadoras de imunodeficiência congênita ou adquirida\n'
        '• Pessoas com doenças crônicas\n'
        '• Pacientes em tratamento de câncer\n'
        '• Transplantados\n'
        '• Pessoas vivendo com HIV\n'
        '• Pessoas em situações especiais de risco\n\n'

        '⚠️ *IMPORTANTE:*\n'
        '• Nem toda condição exige vacina especial\n'
        '• Algumas vacinas estão disponíveis apenas no CRIE\n'
        '• A indicação depende de avaliação clínica\n\n'

        '📌 *Para consultar a UBS mais próxima de você, digite "Localização"*\n\n'
    )
    bot.send_message(user_id, 
        texto, 
        parse_mode='Markdown', 
        reply_markup=botoes_formulario.voltar_grupos_especiais()
        )

def processar_locais_vacinancao_crie(bot, user_id):
    texto = (
        '📍*Locais de vacinação:*\n\n'
        '➡️ Pessoas pertencentes a grupos especiais podem receber vacinas gratuitamente pelo SUS em unidades como UBS, CRIE e CIIE. Para isso é necessário encaminhamento médico das redes de saúde pública ou particular às unidades especializadas.\n\n'
        
        '📌 *Para consultar a UBS mais próxima de você, digite "Localização"*'
    )
    bot.send_message(user_id, 
        texto, 
        parse_mode='Markdown', 
        reply_markup=botoes_formulario.voltar_grupos_especiais()
        )

def processar_rie(bot, user_id):
    texto = (
        '🏥 *A Rede de Imunobiológicos para Pessoas com Situações Especiais (RIE) é formada por:*\n\n'

        '➡️ Centros de Referência para Imunobiológicos Especiais (CRIE)\n\n'

        '➡️ Centros Intermediários de Imunobiológicos Especiais (CIIE)\n\n'

        '➡️ Unidades Básicas de Saúde (UBS)\n\n'


        'Esses serviços trabalham em conjunto para garantir que a população com necessidades especiais em saúde tenha acesso seguro e adequado às vacinas recomendadas.'
    )
    bot.send_message(user_id, 
        texto, 
        parse_mode='Markdown', 
        reply_markup=botoes_formulario.voltar_grupos_especiais()
        )

def processar_fonte_crie(bot, user_id):
    texto = (
        '''
        🔗 Consulte mais informações no site oficial do Ministério da Saúde:

        [Vacinas para Grupos Especiais](https://www.gov.br/saude/pt-br/vacinacao/grupos-especiais)
        '''
    )
    bot.send_message(user_id, 
        texto, 
        parse_mode='Markdown', 
        reply_markup=botoes_formulario.voltar_grupos_especiais()
        )

def processar_voltar_grupos_especiais(bot, user_id):
    return iniciar_grupos_especiais(bot, user_id)