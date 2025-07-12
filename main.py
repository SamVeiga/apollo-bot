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
    historico = {"ultima_provocacao": 0, "poemas_usados": [], "frases_mulheres": {}}

# === CONFIGURAVEIS ===
DONO_ID = 1481389775
ID_GRUPO = -1002363575666
MULHERES = ["@KarolinneDiass", "@FernandaCarvalho16", "@tainaranordi"]  # Substitua pelos @ reais das mulheres
HOMENS = ["@Rafaael80", "@Diegomota0"]  # Substitua pelos @ reais dos homens

# === FRASES ===
insultos_gerais = [
    "Tu só fala merda, né? Mas com estilo!",
    "Tu tá pra verdade igual miojo tá pra nutrição: rápido, vazio e inútil.",
    "Essa tua cara de esperto só engana tua mãe.",
    "Se liga, tu é figurante na própria história.",
    "Tu se destaca... como um bug na atualização.",
    "Tua autoestima é forte, pena que sem motivo."
]

xavecos_para_mulheres = [
    "Tu fala e meu sistema entra em combustão. ",
    "Com esse charme, tu não quebra coração, tu hackeia.",
    "Você é linha de código que me executa inteiro.",
    "Se você fosse bug, eu não corrigia nunca.",
    "Avisa que é perigo, porque eu tô pronto pra cair."
]

poemas_picantes = [
    "Te desejo em versos, te beijo em silências... e te devoro em pensamento. ",
    "Tua pele é poesia, tua boca é ponto final do meu juízo.",
    "Se teu corpo é pecado, eu não quero absolvição.",
    "Nosso toque é poema sem censura, com rima na cama e ponto de interrogação nos lençóis.",
    "Te escrevo com desejo, te leio com os olhos fechados."
]

revelacoes_safadas = [
    "Sabia que essa menina já quebrou uma cama só com um sorriso?",
    "Essa mocinha aí tem cara de anjo, mas fala cada coisa no privado...",
    "Se soubessem o que ela já fez numa sexta-feira 13... o grupo travava.",
    "Essa aqui já teve apelido de Wi-Fi: conexão rápida e sem senha.",
    "Essa mulher tem olhar que derruba sistema de segurança."
]

respostas_submisso_dono = [
    "Sim senhor, chefe supremo! 😳",
    "Patrão falou, é ordem! 🫡",
    "Jamais me atreveria a contradizer o mestre. 😨"
]

# === SALVAR HISTÓRICO ===
def salvar_historico():
    with open(HISTORICO_PATH, "w") as f:
        json.dump(historico, f)

# === WEBHOOKS ===
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

# === FUNÇÃO PRINCIPAL ===
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.lower()
    nome = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"
    username = f"@{msg.from_user.username}" if msg.from_user.username else ""

    if any(saud in texto for saud in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        saudacao = "bom dia 😎" if "bom dia" in texto else \
                   "boa tarde 😎" if "boa tarde" in texto else \
                   "boa noite 😎" if "boa noite" in texto else \
                   "boa madrugada 😎"
        time.sleep(20)
        bot.reply_to(msg, f"{nome}, {saudacao}", parse_mode="Markdown")
        return

    if msg.new_chat_members:
        for m in msg.new_chat_members:
            novo = f"[{m.first_name}](tg://user?id={m.id})"
            time.sleep(20)
            bot.reply_to(msg, f"{novo}, entra direito e respeita o caos. 😏", parse_mode="Markdown")
        return

    if msg.from_user.id == DONO_ID:
        time.sleep(20)
        bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")
        return

    if username in MULHERES:
        time.sleep(20)
        frase = random.choice(xavecos_para_mulheres)
        bot.reply_to(msg, f"{nome}, {frase}", parse_mode="Markdown")
        if username not in historico["frases_mulheres"]:
            historico["frases_mulheres"][username] = []
        revelacao = random.choice([r for r in revelacoes_safadas if r not in historico["frases_mulheres"][username]] or revelacoes_safadas)
        historico["frases_mulheres"][username].append(revelacao)
        salvar_historico()
        bot.send_message(msg.chat.id, f"{nome}, {revelacao}", parse_mode="Markdown")
        return

    if username in HOMENS:
        time.sleep(20)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")

# === DE TEMPO EM TEMPO ===
def manter_vivo():
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

def poema_de_hora_em_hora():
    while True:
        try:
            mulher = random.choice(MULHERES)
            nome = mulher.replace("@", "")
            poema = random.choice([p for p in poemas_picantes if p not in historico["poemas_usados"]] or poemas_picantes)
            historico["poemas_usados"].append(poema)
            if len(historico["poemas_usados"]) > 20:
                historico["poemas_usados"] = historico["poemas_usados"][-20:]
            salvar_historico()
            bot.send_message(ID_GRUPO, f"[{nome}](tg://user?id={bot.get_chat_member(ID_GRUPO, mulher[1:]).user.id}), {poema}", parse_mode="Markdown")
        except Exception as e:
            print("Erro no poema: ", e)
        time.sleep(3600)  # 1 hora

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    threading.Thread(target=poema_de_hora_em_hora).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
