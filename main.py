# ✅ BOT APOLLO REFORMULADO - main.py
# Desenvolvido conforme pedido: tudo em raiz, respostas com menção, frases separadas em .json, submissão ao dono, diferenciado por gênero

from flask import Flask, request
import telebot
import os
import random
import time
import json
import threading
from datetime import datetime, timedelta

# ✅ CONFIGURAÇÕES DO GRUPO
GRUPO_ID = -1002363575666  # Altere para o ID do seu grupo
DONO_ID = 1481389775       # ID do dono (para submissão)
TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ✅ Função para carregar arquivos JSON

def carregar_lista(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# ✅ Carregando todas as listas da raiz
bom_dia_mulher = carregar_lista("bom_dia_mulher.json")
bom_dia_homem = carregar_lista("bom_dia_homem.json")
boa_tarde_mulher = carregar_lista("boa_tarde_mulher.json")
boa_tarde_homem = carregar_lista("boa_tarde_homem.json")
boa_noite_entrada_mulher = carregar_lista("boa_noite_entrada_mulher.json")
boa_noite_entrada_homem = carregar_lista("boa_noite_entrada_homem.json")
boa_noite_dormir_mulher = carregar_lista("boa_noite_dormir_mulher.json")
boa_noite_dormir_homem = carregar_lista("boa_noite_dormir_homem.json")
xavecos = carregar_lista("xavecos.json")
insultos = carregar_lista("insultos.json")
men_m = carregar_lista("menções_mulher.json")
men_h = carregar_lista("menções_homem.json")
frases_dono = carregar_lista("frases_dono.json")
defesa_madonna_homem = carregar_lista("defesa_madonna_homem.json")
defesa_madonna_mulher = carregar_lista("defesa_madonna_mulher.json")

# ✅ IDENTIFICAÇÃO DE GÊNERO POR USERNAME
usuarios_mulheres = carregar_lista("usuarios_mulheres.json")
usuarios_homens = carregar_lista("usuarios_homens.json")

def e_mulher(user):
    username = (user.username or "").lower()
    if username in [u.lower() for u in usuarios_mulheres]:
        return True
    elif username in [u.lower() for u in usuarios_homens]:
        return False
    else:
        # fallback caso não esteja nas listas
        nome = (user.first_name or "").lower()
        return nome[-1] in ["a", "e"]

# ✅ Controle de xaveco/insulto por horário
ultimos_envios = {}

# ✅ Função auxiliar para responder com delay
def responder_com_delay(segundos, func):
    threading.Timer(segundos, func).start()

# ✅ Handler de mensagens recebidas no grupo
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    # ✅ Se quiser restringir o bot para um grupo específico novamente:
    # ➤ Apague os jogos da velha abaixo e certifique-se de que GRUPO_ID está definido corretamente.
    # if msg.chat.id != GRUPO_ID:
    #     return

    texto = msg.text.lower()
    user_id = msg.from_user.id
    nome = msg.from_user.first_name or msg.from_user.username or "Amor"
    mulher = e_mulher(msg.from_user)
    agora = datetime.now()

    # 🔰 Submissão ao DONO (resposta após 60s)
    if user_id == DONO_ID and frases_dono:
        if "apollo" in texto or "@apolo_8bp_bot" in texto:
            responder_com_delay(60, lambda: bot.send_message(
                msg.chat.id, random.choice(frases_dono), reply_to_message_id=msg.message_id
            ))
            return

    # 🔰 Mencionaram o Apollo (resposta após 30 min)
    if "apollo" in texto or f"@{bot.get_me().username.lower()}" in texto:
        if mulher and men_m:
            responder_com_delay(1800, lambda: bot.send_message(
                msg.chat.id, random.choice(men_m), reply_to_message_id=msg.message_id
            ))
        elif not mulher and men_h:
            responder_com_delay(1800, lambda: bot.send_message(
                msg.chat.id, random.choice(men_h), reply_to_message_id=msg.message_id
            ))
        return

            # 🔥 Mencionaram a Madonna
    if "madonna" in texto or "@madonna" in texto:
        if mulher and defesa_madonna_mulher:
            responder_com_delay(15, lambda: bot.send_message(
                msg.chat.id, random.choice(defesa_madonna_mulher), reply_to_message_id=msg.message_id
            ))
        elif not mulher and defesa_madonna_homem:
            responder_com_delay(15, lambda: bot.send_message(
                msg.chat.id, random.choice(defesa_madonna_homem), reply_to_message_id=msg.message_id
            ))
        return

    # 🌞 BOM DIA - 60 segundos
    if "bom dia" in texto:
        frase = random.choice(bom_dia_mulher if mulher else bom_dia_homem)
        responder_com_delay(60, lambda: bot.send_message(
            msg.chat.id, frase, reply_to_message_id=msg.message_id
        ))
        return

    # ☀️ BOA TARDE - 60 segundos
    if "boa tarde" in texto:
        frase = random.choice(boa_tarde_mulher if mulher else boa_tarde_homem)
        responder_com_delay(60, lambda: bot.send_message(
            msg.chat.id, frase, reply_to_message_id=msg.message_id
        ))
        return

    # 🌙 BOA NOITE - 60 segundos
    if "boa noite" in texto or "boa madrugada" in texto:
        if agora.hour < 21:
            frase = random.choice(boa_noite_entrada_mulher if mulher else boa_noite_entrada_homem)
        else:
            frase = random.choice(boa_noite_dormir_mulher if mulher else boa_noite_dormir_homem)
        responder_com_delay(60, lambda: bot.send_message(
            msg.chat.id, frase, reply_to_message_id=msg.message_id
        ))
        return

    # 💬 Xaveco ou insulto após 30 minutos (exceto para o dono)
    if user_id != DONO_ID:
        chave = f"{user_id}_{'mulher' if mulher else 'homem'}"
        if chave not in ultimos_envios or (agora - ultimos_envios[chave]) > timedelta(minutes=30):
            ultimos_envios[chave] = agora
            if mulher and xavecos:
                responder_com_delay(1800, lambda: bot.send_message(
                    msg.chat.id, random.choice(xavecos), reply_to_message_id=msg.message_id
                ))
            elif not mulher and insultos:
                responder_com_delay(1800, lambda: bot.send_message(
                    msg.chat.id, random.choice(insultos), reply_to_message_id=msg.message_id
                ))
            
# 🔁 FLASK API PARA RENDER
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def home():
    url = f"{RENDER_URL}/{TOKEN}"
    if bot.get_webhook_info().url != url:
        bot.remove_webhook()
        bot.set_webhook(url=url)
    return "Apollo online!", 200

# 🔄 Mantém o bot ativo no Render

def manter_vivo():
    import requests
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

# 🚀 INICIAR TUDO
if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
