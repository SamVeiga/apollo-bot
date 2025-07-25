from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests
import json
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from utils.helpers import load_phrases as carregar_json

# === CONFIGURAÇÕES ===
SAUDACOES_ATIVADAS = True
TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === CAMINHOS ===
DIC_PATH = "data/dicionario_apollo.json"
HISTORICO_PATH = "data/historico_apollo.json"

# === DADOS CARREGADOS ===
dicionario = carregar_json(DIC_PATH)
try:
    historico = carregar_json(HISTORICO_PATH)
except:
    historico = {"frases_mulheres": [], "insultos_homens": []}

# === MEMBROS ===
HOMENS = carregar_json("data/membros/homens.json")
MULHERES = carregar_json("data/membros/mulheres.json")

# === FRASES ===
saudacoes_paths = {
    "bom_dia": {
        "homem": "data/frases/saudacoes/bom_dia/homens.json",
        "mulher": "data/frases/saudacoes/bom_dia/mulheres.json"
    },
    "boa_tarde": {
        "homem": "data/frases/saudacoes/boa_tarde/homens.json",
        "mulher": "data/frases/saudacoes/boa_tarde/mulheres.json"
    },
    "boa_noite_entrada": {
        "homem": "data/frases/saudacoes/boa_noite_entrada/homens.json",
        "mulher": "data/frases/saudacoes/boa_noite_entrada/mulheres.json"
    },
    "boa_noite_despedida": {
        "homem": "data/frases/saudacoes/boa_noite_despedida/homens.json",
        "mulher": "data/frases/saudacoes/boa_noite_despedida/mulheres.json"
    }
}

insultos_para_homens = carregar_json("data/frases/insultos_para_homens.json")
xavecos_para_mulheres = carregar_json("data/frases/xavecos_para_mulheres.json")
respostas_submisso_dono = carregar_json("data/frases/respostas_submisso_dono.json")

# === FUNÇÕES ===
def agora_brasilia():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

def salvar_historico():
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def buscar_termo_no_dicionario(texto_original):
    termo_normalizado = texto_original.lower().strip()
    chaves_ordenadas = sorted(dicionario.keys(), key=lambda x: -len(x))
    for chave in chaves_ordenadas:
        if chave in termo_normalizado:
            return random.choice(dicionario[chave])
    return f"Poxa, ainda não sei o que é *{texto_original}*. Mas já tô estudando pra te dizer depois! ✍🏻🤓"

def identificar_genero(username):
    return "mulher" if username in MULHERES else "homem"

def saudacao_do_dia(genero):
    hora = agora_brasilia().hour
    if hora < 12:
        tipo = "bom_dia"
    elif hora < 18:
        tipo = "boa_tarde"
    elif hora < 22:
        tipo = "boa_noite_entrada"
    else:
        tipo = "boa_noite_despedida"
    frases = carregar_json(saudacoes_paths[tipo][genero])
    return random.choice(frases)

def filtrar_frases(frases, tipo):
    agora = agora_brasilia()
    limite = agora - timedelta(days=3)
    usadas_recentemente = [item["frase"] for item in historico.get(tipo, []) if datetime.fromisoformat(item["data"]) >= limite]
    candidatas = [f for f in frases if f not in usadas_recentemente]
    return random.choice(candidatas if candidatas else frases)

def registrar_frase(tipo, frase):
    historico.setdefault(tipo, [])
    historico[tipo].append({"frase": frase, "data": agora_brasilia().isoformat()})
    historico[tipo] = historico[tipo][-200:]  # limita histórico
    salvar_historico()

def pode_responder(usuario, tipo_controle):
    agora = agora_brasilia()
    hoje = agora.date().isoformat()
    historico.setdefault("controle", {})
    historico["controle"].setdefault(tipo_controle, {})
    historico["controle"][tipo_controle].setdefault(usuario, [])
    historico["controle"][tipo_controle][usuario] = [t for t in historico["controle"][tipo_controle][usuario] if t.startswith(hoje)]
    if len(historico["controle"][tipo_controle][usuario]) < 3:
        if not historico["controle"][tipo_controle][usuario] or (agora - datetime.fromisoformat(historico["controle"][tipo_controle][usuario][-1])).total_seconds() > 3600:
            historico["controle"][tipo_controle][usuario].append(agora.isoformat())
            salvar_historico()
            return True
    return False

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
    username = f"@{msg.from_user.username}" if msg.from_user.username else ""
    genero = identificar_genero(username)
    mencionado = any(tag in texto for tag in ["apollo", f"@{bot.get_me().username.lower()}"])

    # 🔽 Adicione estas linhas de debug logo abaixo
    print("==== MENSAGEM RECEBIDA ====")
    print(f"Texto: {texto}")
    print(f"Username: {username}")
    print(f"Gênero detectado: {genero}")
    print(f"Mencionado: {mencionado}")
    print(f"From ID: {msg.from_user.id}")

    pergunta = re.match(r"^@?apollo[, ]*(o que é|significa|define|explica|explique)\s+(.+?)[\?\.!]?$", texto)
    if pergunta:
        termo = pergunta.group(2).strip()
        resposta = buscar_termo_no_dicionario(termo)
        bot.reply_to(msg, resposta, parse_mode="Markdown")
        return

    if msg.from_user.id == int(os.getenv("DONO_ID", 0)) and mencionado:
        frase = filtrar_frases(respostas_submisso_dono, "respostas_submisso_dono")
        registrar_frase("respostas_submisso_dono", frase)
        bot.reply_to(msg, frase, parse_mode="Markdown")
        return

    if username in MULHERES:
        if mencionado or pode_responder(username, "frases_mulheres"):
            frase = filtrar_frases(xavecos_para_mulheres, "frases_mulheres")
            registrar_frase("frases_mulheres", frase)
            bot.reply_to(msg, frase, parse_mode="Markdown")
            return

    if username in HOMENS:
        if mencionado or pode_responder(username, "insultos_homens"):
            frase = filtrar_frases(insultos_para_homens, "insultos_homens")
            registrar_frase("insultos_homens", frase)
            bot.reply_to(msg, frase, parse_mode="Markdown")
            return

    if SAUDACOES_ATIVADAS and any(s in texto for s in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        frase = saudacao_do_dia(genero)
        bot.reply_to(msg, frase, parse_mode="Markdown")
        return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
