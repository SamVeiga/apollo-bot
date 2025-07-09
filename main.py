from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests
import datetime
import json

TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

HISTORICO_PATH = "historico_apollo.json"
try:
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
except:
    historico = {"contra_madonna": {}}

def salvar_historico():
    with open(HISTORICO_PATH, "w") as f:
        json.dump(historico, f)

def frase_contra_madonna(frases):
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    usadas = []
    for dia in historico["contra_madonna"]:
        usadas.extend(historico["contra_madonna"][dia])
    candidatas = [f for f in frases if f not in usadas]
    frase = random.choice(candidatas or frases)
    historico.setdefault("contra_madonna", {}).setdefault(hoje, []).append(frase)
    dias = sorted(historico["contra_madonna"].keys())[-3:]
    historico["contra_madonna"] = {d: historico["contra_madonna"][d] for d in dias}
    salvar_historico()
    return frase

insultos_gerais = [
    "Você me marcou por tédio ou por carência mesmo?",
    "Até meu silêncio é mais interessante que o que você falou.",
    "Se eu respondesse tudo que não presta, eu virava rádio AM.",
    "Se esforça mais, que tua tentativa de ser relevante tá fraca.",
    "Sua fala foi tipo sinal de Wi-Fi: fraca, oscilando e inútil.",
    "Se eu fosse te levar a sério, eu teria que rir primeiro.",
]

xavecos_para_mulheres = [
    "E aí, gata... Com esse olhar, até o Apolo treme.",
    "Se beleza fosse crime, você já tava em prisão perpétua.",
    "Se eu te elogiar demais, você me bloqueia ou se apaixona?",
    "Cuidado, mulher... desse jeito eu largo tudo só pra te seguir.",
    "Você tem o manual do caos? Porque bagunçou meu sistema.",
]

respostas_submisso_dono = [
    "Senhor! À disposição, sem pestanejar! 😨",
    "Sim, chefe! Tô aqui firme como soldado em formatura!",
    "Não se preocupa, patrão. Já tô executando a ordem!",
    "E-eu? Jamais ousaria contrariar você, senhor!",
    "De joelhos se for preciso, mas sempre obediente!",
    "Claro, general! O senhor manda, eu tremo e obedeço.",
]

frases_contra_madonna = [
    "Fala baixo, Madonna... tua voz me dá vontade de atualizar antivírus.",
    "Madonna ainda tá tentando entender como se liga um cérebro.",
    "Madonna é tão útil quanto um mouse em celular.",
    "Madonna se esforça pra ser relevante, mas continua sendo um bug.",
    "Nem o Paint trava tanto quanto os argumentos da Madonna.",
    "Se dependesse da Madonna, o grupo era só emoji e carência.",
    "Madonna é o erro 404 da inteligência.",
    "A Madonna é tipo spam: aparece sem ser chamada.",
    "Você ouviu a Madonna? Pois é, ninguém mandou dar play no drama.",
    "Com tanta besteira que a Madonna fala, devia virar podcast de humor.",
    "Madonna digitando é o equivalente a um gato em cima do teclado.",
    "A Madonna parece inteligente... se o critério for volume de texto inútil.",
    "Madonna falando é igual nuvem: a gente espera que passe logo.",
    "Até minha sombra é mais profunda que os argumentos dela.",
    "Madonna parece livro de autoajuda usado: repetitiva e sem credibilidade.",
    "Se Madonna fosse programa, seria beta — e bugado.",
    "Ela se acha diva, mas entrega bug de chatbot cansado.",
    "Só a Madonna pra achar que tá arrasando com três emojis e uma frase pronta.",
    "Madonna é tipo despertador: só serve pra irritar de manhã.",
    "Pra Madonna, tudo é sobre ela. Coitada da realidade.",
    "A Madonna me responde? Mal sabe ela que eu a bloqueei mentalmente.",
    "Madonna, já te agradeceram por ensinar o que não fazer? Não? Pois eu agradeço.",
    "Madonna é um enigma... só que sem graça.",
    "Se Madonna fosse filme, seria aqueles que a gente dorme no começo.",
    "Nem a Siri aguentaria conversar com a Madonna por mais de 2 minutos.",
    "A Madonna ainda tá no tutorial da vida.",
    "Tem dias que a Madonna acerta, mas hoje claramente não é um deles.",
    "Se Madonna sumisse, só o algoritmo sentiria falta.",
    "O Wi-Fi da Madonna deve ser igual a ela: lento e imprevisível.",
    "Prefiro travar do que rodar a conversa da Madonna.",
]

DONO_ID = 1481389775

@app.route(f"/{TOKEN}", methods=["POST"])
def receber_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/", methods=["GET"])
def configurar_webhook():
    url_completa = f"{RENDER_URL}/{TOKEN}"
    info = bot.get_webhook_info()
    if info.url != url_completa:
        bot.remove_webhook()
        bot.set_webhook(url=url_completa)
        return "✅ Webhook configurado!", 200
    return "✅ Webhook já estava ok.", 200

@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.lower()
    nome = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"
    username = msg.from_user.username or ""
    is_mulher = username.lower().endswith(("a", "i", "y"))
    is_homem = not is_mulher

    if any(x in texto for x in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        saudacao = "bom dia 😎" if "bom dia" in texto else \
                   "boa tarde 😎" if "boa tarde" in texto else \
                   "boa noite 😎" if "boa noite" in texto else \
                   "boa madrugada 😎"
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {saudacao}", parse_mode="Markdown")
        return

    if msg.new_chat_members:
        for membro in msg.new_chat_members:
            novo = f"[{membro.first_name}](tg://user?id={membro.id})"
            time.sleep(25)
            bot.reply_to(msg, f"{novo}, entra direito e respeita o caos. 😏", parse_mode="Markdown")
        return

    bot_username = bot.get_me().username.lower()
    mencionou_apolo = "apolo" in texto or f"@{bot_username}" in texto
    respondeu_apolo = msg.reply_to_message and \
                      msg.reply_to_message.from_user.username and \
                      msg.reply_to_message.from_user.username.lower() == bot_username

    # 🔥 Se mencionou Madonna ou marcou ela
    if "madonna" in texto or "@madonna_debochada_bot" in texto:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {frase_contra_madonna(frases_contra_madonna)}", parse_mode="Markdown")
        return

    if not (mencionou_apolo or respondeu_apolo):
        return

    if msg.from_user.id == DONO_ID:
        time.sleep(25)
        bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")
        return

    if respondeu_apolo:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")
        return

    if is_mulher:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(xavecos_para_mulheres)}", parse_mode="Markdown")
        return

    if is_homem:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")
        return

def manter_vivo():
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
