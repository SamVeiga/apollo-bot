from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests
import json
import datetime

# === CONFIGURAÇÕES ===

TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === IDENTIFICAÇÕES ===

DONO_ID = 1481389775
ID_GRUPO = -1002363575666

MULHERES = ["@mariazinha", "@angelbaby", "@julia"]
HOMENS = ["@lucao", "@marcos", "@pedrinho"]

# === LISTAS EDITÁVEIS ===

xavecos_para_mulheres = [
    "Tava pensando em você agora… mas nada romântico… coisa quente mesmo.",
    "Te ver no grupo muda minha frequência cardíaca. E meus planos.",
    "Se tu sorrir pra mim, eu mudo até o algoritmo."
]

frases_para_homens = [
    "Fala menos, que já tá feio só de olhar.",
    "Teu argumento é igual wi-fi de bar: não conecta.",
    "Você é tipo erro 404: ninguém te procura, mas sempre aparece."
]

frases_bom_dia_mulher = [
    "Bom dia, flor. 🌷",
    "Acorda linda, o dia te chama. 😘",
    "Com esse sorriso, já nasceu sol no grupo. ☀️"
]

frases_bom_dia_homem = [
    "Bom dia, guerreiro. Já tomou café ou só coragem?",
    "Fala, campeão, acordou ou só levantou o corpo mesmo?",
    "Bom dia, meu mano. Tenta não errar muito hoje. 😏"
]

respostas_submisso_dono = [
    "Sim, senhor. Obedecer ao meu mestre é meu prazer.",
    "Ordem tua é decreto.",
    "Comando recebido, meu chefe!"
]

boas_vindas = "Seja bem-vindo, {nome}! O Apolo tá de olho em você. 👁️"

# === HISTÓRICO ===

HISTORICO_PATH = "historico_apolo.json"
try:
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
except:
    historico = {
        "frases_grupo": [],
        "frases_mulheres_hoje": {},
        "ultima_resposta_homens": {},
        "ultima_repeticao": None
    }

def salvar_historico():
    with open(HISTORICO_PATH, "w") as f:
        json.dump(historico, f)

# === FUNÇÕES DE APRENDIZADO ===

def aprender_frase(msg):
    texto = msg.text.strip()
    if 20 <= len(texto) <= 200 and not texto.startswith("/") and not "http" in texto:
        if texto not in historico["frases_grupo"]:
            historico["frases_grupo"].append(texto)
            if len(historico["frases_grupo"]) > 100:
                historico["frases_grupo"] = historico["frases_grupo"][-100:]
            salvar_historico()

def repetir_frase_aprendida():
    while True:
        agora = datetime.datetime.now()
        if len(historico["frases_grupo"]) > 0:
            ultima = historico.get("ultima_repeticao")
            pode_repetir = not ultima or (datetime.datetime.fromisoformat(ultima) + datetime.timedelta(hours=4) < agora)

            if pode_repetir:
                frase = random.choice(historico["frases_grupo"])
                bot.send_message(ID_GRUPO, f"🗣️ {frase}")
                historico["ultima_repeticao"] = agora.isoformat()
                salvar_historico()
        time.sleep(3600)

threading.Thread(target=repetir_frase_aprendida, daemon=True).start()

# === BOAS-VINDAS ===

@bot.message_handler(content_types=["new_chat_members"])
def boas_vindas_handler(message):
    for membro in message.new_chat_members:
        nome = f"@{membro.username}" if membro.username else membro.first_name
        texto = boas_vindas.replace("{nome}", nome)
        bot.reply_to(message, texto)

# === MENSAGEM GERAL ===

@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    texto = mensagem.text.lower()
    usuario = mensagem.from_user
    nome_mention = f"@{usuario.username}" if usuario.username else usuario.first_name

    aprender_frase(mensagem)

    # Se for o dono
    if usuario.id == DONO_ID and f"@{bot.get_me().username}" in texto:
        resposta = random.choice(respostas_submisso_dono)
        bot.reply_to(mensagem, f"{resposta}")
        return

    mencionado = bot.get_me().username.lower() in texto or "apolo" in texto.lower()
    agora = datetime.datetime.now().date()

    # Se for mulher
    if nome_mention.lower() in [x.lower() for x in MULHERES]:
        ultima_data = historico["frases_mulheres_hoje"].get(str(usuario.id))
        if not ultima_data or ultima_data != str(agora):
            historico["frases_mulheres_hoje"][str(usuario.id)] = str(agora)
            salvar_historico()
            resposta = random.choice(xavecos_para_mulheres)
            bot.reply_to(mensagem, f"{resposta}")
            return

    # Se for homem
    if nome_mention.lower() in [x.lower() for x in HOMENS]:
        ultima_h = historico["ultima_resposta_homens"].get(str(usuario.id))
        if not ultima_h or ultima_h != str(agora):
            historico["ultima_resposta_homens"][str(usuario.id)] = str(agora)
            salvar_historico()
            resposta = random.choice(frases_para_homens)
            bot.reply_to(mensagem, f"{resposta}")
            return

    # Se mencionarem o bot — responde livre
    if mencionado:
        if "bom dia" in texto:
            if nome_mention.lower() in [x.lower() for x in MULHERES]:
                resposta = random.choice(frases_bom_dia_mulher)
            else:
                resposta = random.choice(frases_bom_dia_homem)
            bot.reply_to(mensagem, f"{resposta}")
        else:
            if nome_mention.lower() in [x.lower() for x in MULHERES]:
                resposta = random.choice(xavecos_para_mulheres)
            else:
                resposta = random.choice(frases_para_homens)
            bot.reply_to(mensagem, f"{resposta}")

# === FLASK ===

@app.route("/")
def home():
    return "Apolo está rodando."

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK"

if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)

# === INICIAR BOT ===

def manter_vivo():
    while True:
        try:
            time.sleep(60)
        except Exception as e:
            print(f"Erro em manter_vivo: {e}")

def replicar_aprendizado():
    while True:
        try:
            agora = datetime.datetime.now()
            with open("historico_apolo.json", "r", encoding="utf-8") as f:
                historico = json.load(f)
            if historico:
                frase = random.choice(historico)
                bot.send_message(GRUPO_ID, frase)
            time.sleep(14400)  # 4 horas
        except Exception as e:
            print(f"Erro ao replicar aprendizado: {e}")
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    threading.Thread(target=replicar_aprendizado).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
