from flask import Flask, request
import telebot
import random
import time
import threading
import json
import os
from datetime import datetime, timedelta

TOKEN = '7559286879:AAFSeGER9vX0Yav0l5L0s7fzz3OvVVOhZPg'
DONO_USERNAME = "samuel_gpm"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

HISTORICO_PATH = "frases_usadas.json"

# Frases por perfil
FRASES_GERAIS = [
    "Ironia é quando a inteligência resolve brincar.",
    "Confuso? Calma, é só a realidade passando sem aviso.",
    "Deboche é o tempero da sabedoria preguiçosa.",
    "Quem tem cérebro, pensa. Quem tem estilo, debocha.",
    "Essa lógica aí é compatível com magia caótica.",
]

FRASES_ROMANTICAS = [
    "Se beleza fosse argumento, você calaria o grupo.",
    "Com essa inteligência e esse charme, você me desmonta.",
    "Nem a filosofia explica esse impacto que você tem em mim.",
    "Você é tipo ideia boa: rara, surpreendente e encantadora.",
    "Se você fosse tese, eu passava a vida tentando te defender.",
]

FRASES_IRONICAS = [
    "Esse argumento seu foi tipo update bugado: travou tudo.",
    "Tem lógica aí? Porque passou batido aqui.",
    "Se o ridículo fosse profissão, já tinha carteira assinada.",
    "Você fala com tanta certeza... de que tá errado.",
    "Ironia é te responder como se fosse sério.",
]

FRASES_BAJULACAO = [
    "Se o Apolo fala, o Samuel reina. Ordem natural das coisas.",
    "Grupo bom é grupo com Samuel presente. O resto só acompanha.",
    "Diante de Samuel, até os deuses da sabedoria se calam.",
    "Samuel não é só o dono, é o dono da moral e da estética.",
    "Por onde Samuel passa, o respeito se organiza.",
]

FRASES_RISADA = [
    "kkkkkk", "rachei aqui", "essa foi digna de uma tese de humor",
    "rindo alto igual filósofo bêbado", "hahaha, melhor que debate acadêmico"
]

FRASES_SAUDACOES = [
    "Bom dia com café e sarcasmo.",
    "Boa tarde pra quem pensa antes de digitar.",
    "Boa noite, menos pra quem compartilha fake news.",
    "Boa madrugada, filósofos insones.",
]

# Garante arquivo de histórico
if not os.path.exists(HISTORICO_PATH):
    with open(HISTORICO_PATH, "w") as f:
        json.dump({}, f)

def carregar_historico():
    with open(HISTORICO_PATH, "r") as f:
        return json.load(f)

def salvar_historico(data):
    with open(HISTORICO_PATH, "w") as f:
        json.dump(data, f)

def gerar_frases_do_dia():
    hoje = datetime.now().date().isoformat()
    historico = carregar_historico()
    dias_validos = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(1, 4)]
    usadas_recentemente = set()
    for dia in dias_validos:
        usadas_recentemente.update(historico.get(dia, []))

    candidatas = list(set(FRASES_GERAIS + FRASES_ROMANTICAS + FRASES_IRONICAS) - usadas_recentemente)
    random.shuffle(candidatas)
    frases_do_dia = candidatas[:100]
    historico[hoje] = frases_do_dia
    salvar_historico(historico)
    return frases_do_dia

FRASES_HOJE = gerar_frases_do_dia()
FRASE_INDEX = 0

def responder_com_delay(mensagem, texto):
    def esperar():
        time.sleep(30)
        bot.reply_to(mensagem, texto)
    threading.Thread(target=esperar).start()

def is_saudacao(texto):
    return any(p in texto for p in ['bom dia', 'boa tarde', 'boa noite', 'boa madrugada'])

def is_risada(texto):
    return any(p in texto for p in ['kkk', 'rs', 'haha', 'heue'])

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "Apolo está vivo e debochado 😎", 200

@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    global FRASE_INDEX
    texto = mensagem.text.lower()
    citado = (mensagem.chat.type != "private") and (bot.get_me().username.lower() in texto or 'apolo' in texto)
    nome = mensagem.from_user.first_name
    username = mensagem.from_user.username or ""
    eh_mulher = mensagem.from_user.is_bot == False and mensagem.from_user.username and mensagem.from_user.username.endswith("a")
    eh_dono = username.lower() == DONO_USERNAME.lower()

    # Boas-vindas
    if mensagem.new_chat_members:
        nome_novo = mensagem.new_chat_members[0].first_name
        responder_com_delay(mensagem, f"Bem-vindo ao caos, {nome_novo}. Sinta-se ignorado com classe.")
        return

    # Risadas
    if is_risada(texto):
        responder_com_delay(mensagem, random.choice(FRASES_RISADA))
        return

    # Saudações
    if is_saudacao(texto):
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, FRASES_HOJE[FRASE_INDEX])
            FRASE_INDEX += 1
        return

    # Só responde se for mencionado ou citado
    if not citado:
        return

    # Bajulação do dono
    if eh_dono:
        frase = random.choice(FRASES_BAJULACAO)
    # Mulheres recebem cantadas
    elif eh_mulher:
        frase = random.choice(FRASES_ROMANTICAS)
    # Homens recebem ironia
    else:
        frase = random.choice(FRASES_IRONICAS)

    responder_com_delay(mensagem, f"{nome}, {frase}")

if __name__ == "__main__":
    with app.app_context():
        bot.remove_webhook()
        bot.set_webhook(url=f"https://apollo-bot.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
