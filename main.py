from flask import Flask, request
import telebot
import random
import time
import threading
import json
import os
from datetime import datetime, timedelta

TOKEN = '7559286879:AAFSeGER9vX0Yav0l5L0s7fzz3OvVVOhZPg'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Arquivo com histórico de frases usadas
HISTORICO_PATH = "frases_usadas.json"

# Frases base do Apolo
TODAS_AS_FRASES = [
    "Ironia é quando a inteligência resolve brincar.",
    "Nem toda resposta precisa de uma pergunta sensata.",
    "Até Platão sairia do grupo com essa conversa.",
    "Essa frase foi trazida por Hermes, o deus das indiretas.",
    "Se for pra causar, que seja com argumento.",
    "A mente voa. Pena que o Wi-Fi não acompanha.",
    "Nietzsche teria um infarto lendo essa conversa.",
    "Confuso? Calma, é só a realidade passando sem aviso.",
    "Mais perdido que Descartes em aula de zumba.",
    "Ideia brilhante... pena que não foi a sua.",
    "Quem tem cérebro, pensa. Quem tem estilo, debocha.",
    "Se a ideia é ruim, pelo menos que seja estilosa.",
    "Essa lógica aí é compatível com magia caótica.",
    "Dúvidas são bem-vindas. As suas, eu ignoro.",
    "O grupo é livre. As ideias, nem tanto.",
    "Paradoxo do dia: estou online, mas indisponível.",
    "Sócrates perguntou. Eu respondi com meme.",
    "O sarcasmo é meu idioma secundário. O primário é genialidade.",
    "Rindo alto igual filósofo bêbado.",
] + [f"Frase número {i+81}, sem sentido, porém com estilo." for i in range(70)]

# Garante que arquivo de histórico existe
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

    candidatas = list(set(TODAS_AS_FRASES) - usadas_recentemente)
    random.shuffle(candidatas)
    frases_do_dia = candidatas[:100]

    historico[hoje] = frases_do_dia
    salvar_historico(historico)
    return frases_do_dia

FRASES_HOJE = gerar_frases_do_dia()
FRASE_INDEX = 0

def responder_com_delay(mensagem, texto):
    def esperar_e_responder():
        time.sleep(30)
        bot.reply_to(mensagem, texto)
    threading.Thread(target=esperar_e_responder).start()

def is_saudacao(texto):
    return any(p in texto for p in ['bom dia', 'boa tarde', 'boa noite', 'boa madrugada'])

def is_risada(texto):
    return any(p in texto for p in ['kkk', 'rs', 'haha', 'heue'])

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def index():
    return "Apolo está vivo e debochado 😎", 200

@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    global FRASE_INDEX
    texto = mensagem.text.lower()
    citado = (mensagem.chat.type != "private") and (bot.get_me().username.lower() in texto or 'apolo' in texto)

    if is_saudacao(texto):
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, FRASES_HOJE[FRASE_INDEX])
            FRASE_INDEX += 1
    elif mensagem.new_chat_members:
        nome = mensagem.new_chat_members[0].first_name
        responder_com_delay(mensagem, f"Bem-vindo ao caos, {nome}. Sinta-se ignorado com classe.")
    elif is_risada(texto):
        responder_com_delay(mensagem, random.choice([
            "kkkkkk", "rachei aqui", "hahaha", "essa foi digna de uma tese de humor", "rindo alto igual filósofo bêbado"
        ]))
    elif citado:
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, FRASES_HOJE[FRASE_INDEX])
            FRASE_INDEX += 1

if __name__ == "__main__":
    with app.app_context():
        bot.remove_webhook()
        bot.set_webhook(url=f"https://apollo-bot.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
