from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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

DONO_ID = 1481389775

# === Webhook para manter online ===
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

# === Lógica de resposta ===
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.lower()
    nome = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"
    username = msg.from_user.username or ""
    is_mulher = username.lower().endswith(("a", "i", "y"))
    is_homem = not is_mulher

    # ✅ Saudações com delay e resposta direta
    if any(x in texto for x in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        saudacao = "bom dia 😎" if "bom dia" in texto else \
                   "boa tarde 😎" if "boa tarde" in texto else \
                   "boa noite 😎" if "boa noite" in texto else \
                   "boa madrugada 😎"
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {saudacao}", parse_mode="Markdown")
        return

    # ✅ Boas-vindas automáticas
    if msg.new_chat_members:
        for membro in msg.new_chat_members:
            novo = f"[{membro.first_name}](tg://user?id={membro.id})"
            time.sleep(25)
            bot.reply_to(msg, f"{novo}, entra direito e respeita o caos. 😏", parse_mode="Markdown")
        return

    # ✅ Ignorar se não mencionar o bot
    bot_username = context.bot.username.lower()
mencao_direta = "apolo" in texto or f"@{bot_username}" in texto
resposta_para_apolo = message.reply_to_message and message.reply_to_message.from_user.username == bot_username

if mencao_direta or resposta_para_apolo:
        return

    # ✅ Submissão ao dono
    if msg.from_user.id == DONO_ID:
        time.sleep(25)
        bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")
        return

    # ✅ Se responder o Apolo, ele rebate também
    if msg.reply_to_message and msg.reply_to_message.from_user.username == bot.get_me().username:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")
        return

    # ✅ Xavecos para mulheres
    if is_mulher:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(xavecos_para_mulheres)}", parse_mode="Markdown")
        return

    # ✅ Cortadas nos caras
    if is_homem:
        time.sleep(25)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")
        return

# === Ping automático para manter o bot ativo ===
def manter_vivo():
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

# === Inicialização ===
if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
