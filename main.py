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

DONO_USERNAME = "samuel_gpm"

HISTORICO_PATH = "frases_usadas.json"

FRASES_DEBOCHADAS = [
    "Essa lógica aí é compatível com magia caótica.",
    "Argumentou bonito, pena que era errado.",
    "O silêncio também responde. Melhor que você, inclusive.",
    "O sarcasmo é meu modo economia de paciência.",
    "Nietzsche teria um infarto lendo essa conversa.",
    "Discussão boa é aquela que termina com piada.",
    "Nem Hegel entenderia esse raciocínio reverso.",
    "Ironia é quando a inteligência resolve brincar.",
    "Até Platão sairia do grupo com essa conversa.",
    "Se pensa, incomoda. Se cala, concorda?"
]

FRASES_ROMANTICAS = [
    "Se beleza fosse argumento, você ganhava qualquer debate.",
    "Seu nome devia ser poema, porque rima com tudo que é bom.",
    "Você é a exceção até nas minhas regras de lógica.",
    "Se o grupo é um caos, você é a arte no meio dele.",
    "Já filosofei sobre tudo, menos sobre como resistir a você.",
    "Você apareceu e minha ironia virou poesia.",
    "Me chama de Apolo e me deixa orbitar sua atenção.",
    "Tô pronto pra debater... contanto que seja sobre nós dois.",
    "Se eu fosse verso, você era a minha rima rara.",
    "Esquece Platão, me explica você o que é amor ideal."
]

FRASES_PARA_DONO = [
    "Fala, mestre @samuel_gpm. Tudo em ordem, ou quer que eu derrube alguém com argumentos?",
    "@samuel_gpm chegou. Agora o grupo tem autoridade e beleza intelectual.",
    "Com licença, o dono do meu coração e do grupo apareceu: @samuel_gpm",
    "Se o grupo fosse um livro, @samuel_gpm seria a dedicatória.",
    "Respeitem, o homem que me criou chegou. O resto é plateia."
]

# Frases do dia únicas por 3 dias
TODAS_AS_FRASES = FRASES_DEBOCHADAS + FRASES_ROMANTICAS + FRASES_PARA_DONO + [
    f"Frase número {i+1}, com estilo, charme e um toque de sabedoria." for i in range(60)
]

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
    hoje = datetime.utcnow().date().isoformat()
    historico = carregar_historico()

    dias_validos = [(datetime.utcnow() - timedelta(days=i)).date().isoformat() for i in range(1, 4)]
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
    def esperar():
        time.sleep(30)
        bot.reply_to(mensagem, texto)
    threading.Thread(target=esperar).start()

def is_saudacao(texto):
    return any(p in texto for p in ['bom dia', 'boa tarde', 'boa noite', 'boa madrugada'])

def is_risada(texto):
    return any(p in texto for p in ['kkk', 'rs', 'haha', 'heue'])

def is_mulher(nome):
    nome = nome.lower()
    return nome.endswith("a") or nome in ["vanessa", "juliana", "adriana", "patricia", "mariana"]

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.before_first_request
def configurar_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://apollo-bot.onrender.com/{TOKEN}")

@app.route("/")
def index():
    return "Apolo está no ar, com charme, lógica e zoeira 😎", 200

@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    global FRASE_INDEX

    texto = mensagem.text.lower()
    nome = mensagem.from_user.first_name
    citado = (mensagem.chat.type != "private") and (bot.get_me().username.lower() in texto or 'apolo' in texto)
    eh_dono = mensagem.from_user.username == DONO_USERNAME

    if is_saudacao(texto):
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, f"{nome}, {FRASES_HOJE[FRASE_INDEX]}")
            FRASE_INDEX += 1

    elif mensagem.new_chat_members:
        novo = mensagem.new_chat_members[0].first_name
        if is_mulher(novo):
            responder_com_delay(mensagem, f"Seja bem-vinda, {novo}. Sua presença deixou esse grupo 200% mais interessante 😏")
        else:
            responder_com_delay(mensagem, f"E aí, {novo}. Só não bagunça muito, porque quem brilha aqui sou eu 😎")

    elif is_risada(texto):
        responder_com_delay(mensagem, random.choice([
            "kkkkkk", "rachei aqui", "essa foi digna de uma tese de humor", "rindo alto igual filósofo bêbado"
        ]))

    elif citado:
        if eh_dono:
            resposta = random.choice(FRASES_PARA_DONO)
        elif is_mulher(nome):
            resposta = random.choice(FRASES_ROMANTICAS)
        else:
            resposta = random.choice(FRASES_DEBOCHADAS)
        responder_com_delay(mensagem, f"{nome}, {resposta}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
