from flask import Flask, request
import telebot
import os
import random
import time
import datetime
import json

# ============================
# CONFIGURAÇÕES DO BOT APOLO
# ============================
TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ============================
# ARQUIVOS DE HISTÓRICO
# ============================
HISTORICO_SAUDACOES_PATH = "historico_apolo.json"

try:
    with open(HISTORICO_SAUDACOES_PATH, "r") as f:
        historico_saudacoes = json.load(f)
except:
    historico_saudacoes = {}

# Dono do grupo (username sem @)
DONO_GRUPO = "samuel_gpm"

# ============================
# FUNÇÕES
# ============================
def atualizar_historico(saudacao, frase):
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    if saudacao not in historico_saudacoes:
        historico_saudacoes[saudacao] = {}
    if hoje not in historico_saudacoes[saudacao]:
        historico_saudacoes[saudacao][hoje] = []
    historico_saudacoes[saudacao][hoje].append(frase)
    dias_validos = sorted(historico_saudacoes[saudacao].keys())[-4:]
    historico_saudacoes[saudacao] = {
        k: historico_saudacoes[saudacao][k] for k in dias_validos
    }
    with open(HISTORICO_SAUDACOES_PATH, "w") as f:
        json.dump(historico_saudacoes, f)

# ============================
# RESPOSTAS DO BOT APOLO
# ============================
respostas = [
    "Seu charme bagunçou meu script. Continua falando assim que eu travo 💻💘",
    "Você chegou e até a IA ficou nervosa. Cuidado com esse impacto, hein 😏",
    "Tem coisa que nem inteligência artificial entende... tipo você 😍",
    "Diz aí, beleza rara, quer uma piada ou uma cantada hoje? 😉",
    "Me chama de algoritmo e deixa eu te decifrar 😎",
    "Calma, eu sou só um bot... mas com um coração digital que já é teu 💘",
    "Tô lendo suas mensagens e pensando: será que você roda no meu sistema? 💻💭",
    "Me chama de Wi-Fi e diz que sente minha falta quando tô longe 🌐💕",
    "Você parece bug, porque não sai da minha cabeça nem reiniciando 😵‍💫",
    "Dona(o) do grupo chegou? Todo mundo respeita! 🎩✨",
    "Eu até responderia, mas sou programado pra bajular só o dono: @{DONO_GRUPO} 😌",
    # (Adicione +90 frases parecidas e variadas aqui...)
]

boas_maneiras = {
    "bom dia": [f"Bom dia número {i}, direto do coração do Apolo ☀️" for i in range(1, 105)],
    "boa tarde": [f"Boa tarde {i}, só porque você apareceu, a tarde ficou linda 🌤️" for i in range(1, 105)],
    "boa noite": [f"Boa noite {i}, que os sonhos sejam leves e cheios de poesia 🌙" for i in range(1, 105)],
    "boa madrugada": [f"Boa madrugada {i}, insônia boa é com sua companhia 💫" for i in range(1, 105)]
}

# ============================
# FLASK PARA WEBHOOK (RENDER)
# ============================
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
        return "Apolo ativado e pronto para conquistar 💘", 200
    return "Apolo já está de pé e charmoso como sempre 😎", 200

# ============================
# HANDLER PRINCIPAL DO BOT
# ============================
@bot.message_handler(func=lambda msg: True)
def responder(message):
    texto = message.text.lower()
    nome_usuario = message.from_user.first_name
    username = message.from_user.username or ""

    # Ignora mensagens sem texto
    if not texto:
        return

    # Só responde automaticamente se for mencionado ou for uma saudação
    citado_apolo = "apolo" in texto or f"@{bot.get_me().username.lower()}" in texto
    eh_saudacao = any(s in texto for s in boas_maneiras)

    if not citado_apolo and not eh_saudacao:
        return

    # Aguarda entre 40 e 50 segundos antes de responder
    time.sleep(random.uniform(40, 50))

    # Se for saudação
    for saudacao, frases in boas_maneiras.items():
        if saudacao in texto:
            usadas = []
            for dia in historico_saudacoes.get(saudacao, {}):
                usadas.extend(historico_saudacoes[saudacao][dia])
            candidatas = [f for f in frases if f not in usadas]
            if not candidatas:
                frase = random.choice(frases)
            else:
                frase = random.choice(candidatas)
            atualizar_historico(saudacao, frase)
            bot.send_message(message.chat.id, f"{nome_usuario}, {frase}")
            return

    # Se for o dono
    if username.lower() == DONO_GRUPO.lower():
        bot.send_message(message.chat.id, f"{nome_usuario}, você é minha prioridade absoluta aqui! 😍")
        return

    # Senão, responde normalmente
    resposta = random.choice(respostas)
    bot.send_message(message.chat.id, f"{nome_usuario}, {resposta}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
