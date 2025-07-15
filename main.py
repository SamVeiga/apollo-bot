from flask import Flask, request
import telebot
import os
import random
import time
import threading
import datetime
import json

# === CONFIG ===

TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DONO_ID = 1481389775
ID_GRUPO = -1002363575666

# === LISTAS DE USUÁRIOS ===

MULHERES = ["@FernandaCarvalho16", "@KarolinneDiass", "@Adriannaleal", "@gabrielyandrad", "@vanessapraado", "@tainaranordi", "@sj_photographia"]
HOMENS = ["@MatheusMatano", "@Tomazitc", "@Diegomota0", "@Rafaael80"]

# === FRASES EDITÁVEIS ===

xavecos_mulheres = [
    "Tava pensando em você agora… mas nada romântico… coisa quente mesmo.",
    "Te ver no grupo muda minha frequência cardíaca. E meus planos.",
    "Se tu sorrir pra mim, eu mudo até o algoritmo."
]

deboches_homens = [
    "Fala menos, que já tá feio só de olhar.",
    "Teu argumento é igual wi-fi de bar: não conecta.",
    "Você é tipo erro 404: ninguém te procura, mas sempre aparece."
]

bom_dia_mulher = [
    "Bom dia, flor. 🌷",
    "Acorda linda, o dia te chama. 😘",
    "Com esse sorriso, já nasceu sol no grupo. ☀️"
]

bom_dia_homem = [
    "Bom dia, guerreiro. Já tomou café ou só coragem?",
    "Fala, campeão, acordou ou só levantou o corpo mesmo?",
    "Bom dia, meu mano. Tenta não errar muito hoje. 😏"
]

respostas_submisso_dono = [
    "Sim, senhor. Obedecer ao meu mestre é meu prazer.",
    "Ordem tua é decreto.",
    "Comando recebido, meu chefe!"
]

texto_boas_vindas = "Seja bem-vindo, {nome}! O Apolo tá de olho em você. 👁️"

# === HISTÓRICO ===

HIST_PATH = "historico_apolo.json"
try:
    with open(HIST_PATH, "r", encoding="utf-8") as f:
        historico = json.load(f)
except:
    historico = {
        "frases_grupo": [],
        "frases_mulheres_hoje": {},
        "respostas_homens_hoje": {},
        "ultima_repeticao": None,
        "elogios_anteriores": {},
        "insultos_anteriores": {}
    }

def salvar_historico():
    with open(HIST_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False)

# === APRENDIZADO ===

def aprender_frase(msg):
    conteudo = msg.text or msg.caption or ""
    if 10 <= len(conteudo) <= 300 and not conteudo.startswith("/") and "http" not in conteudo:
        if conteudo not in historico["frases_grupo"]:
            historico["frases_grupo"].append(conteudo)
            historico["frases_grupo"] = historico["frases_grupo"][-200:]
            salvar_historico()

# === REPLICAR APRENDIZADO A CADA 4 HORAS ===

def repetir_frases():
    while True:
        agora = datetime.datetime.now()
        ultima = historico.get("ultima_repeticao")
        pode = not ultima or (datetime.datetime.fromisoformat(ultima) + datetime.timedelta(hours=4) < agora)
        if pode and historico["frases_grupo"]:
            frase = random.choice(historico["frases_grupo"])
            bot.send_message(ID_GRUPO, f"🗣️ {frase}")
            historico["ultima_repeticao"] = agora.isoformat()
            salvar_historico()
        time.sleep(3600)

# === BOAS-VINDAS ===

@bot.message_handler(content_types=["new_chat_members"])
def boas_vindas(mensagem):
    for membro in mensagem.new_chat_members:
        nome = f"@{membro.username}" if membro.username else membro.first_name
        bot.reply_to(mensagem, texto_boas_vindas.replace("{nome}", nome))

# === RESPOSTAS INTELIGENTES ===

@bot.message_handler(func=lambda msg: True, content_types=["text", "audio", "voice", "photo", "sticker"])
def responder(msg):
    usuario = msg.from_user
    texto = (msg.text or msg.caption or "").lower()
    nome = f"@{usuario.username}" if usuario.username else usuario.first_name
    mencionado = f"@{bot.get_me().username}".lower() in texto or "apolo" in texto

    aprender_frase(msg)
    hoje = str(datetime.datetime.now().date())

    if usuario.id == DONO_ID and mencionado:
        resposta = random.choice(respostas_submisso_dono)
        bot.reply_to(msg, resposta)
        return

    if nome.lower() in [m.lower() for m in MULHERES]:
        ultima = historico["frases_mulheres_hoje"].get(str(usuario.id))
        usadas = historico["elogios_anteriores"].get(str(usuario.id), [])
        candidatas = [f for f in xavecos_mulheres if f not in usadas]
        if not candidatas:
            candidatas = xavecos_mulheres
            usadas = []
        if ultima != hoje:
            frase = random.choice(candidatas)
            usadas.append(frase)
            historico["frases_mulheres_hoje"][str(usuario.id)] = hoje
            historico["elogios_anteriores"][str(usuario.id)] = usadas[-3:]  # evita repetir nos 3 dias
            salvar_historico()
            bot.reply_to(msg, frase)
            return

    if nome.lower() in [h.lower() for h in HOMENS]:
        ultima = historico["respostas_homens_hoje"].get(str(usuario.id))
        usadas = historico["insultos_anteriores"].get(str(usuario.id), [])
        candidatas = [f for f in deboches_homens if f not in usadas]
        if not candidatas:
            candidatas = deboches_homens
            usadas = []
        if ultima != hoje:
            frase = random.choice(candidatas)
            usadas.append(frase)
            historico["respostas_homens_hoje"][str(usuario.id)] = hoje
            historico["insultos_anteriores"][str(usuario.id)] = usadas[-3:]
            salvar_historico()
            bot.reply_to(msg, frase)
            return

    if mencionado:
        if "bom dia" in texto:
            if nome.lower() in [m.lower() for m in MULHERES]:
                resposta = random.choice(bom_dia_mulher)
            else:
                resposta = random.choice(bom_dia_homem)
        else:
            if nome.lower() in [m.lower() for m in MULHERES]:
                resposta = random.choice(xavecos_mulheres)
            else:
                resposta = random.choice(deboches_homens)
        bot.reply_to(msg, resposta)

# === FLASK E THREADS ===

@app.route("/")
def home():
    return "Apolo está vivo."

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK"

def manter_vivo():
    while True:
        try:
            time.sleep(60)
        except Exception as e:
            print(f"[ERRO manter_vivo]: {e}")

# === INICIALIZAÇÃO ===

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    threading.Thread(target=repetir_frases, daemon=True).start()
    if RENDER_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        bot.remove_webhook()
        bot.polling(none_stop=True)
