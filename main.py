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

MULHERES = ["@FernandaCarvalho16", "@KarolinneDiass", "@Adriannaleal", "@gabrielyandrad", "@vanessapraado", "@tainaranordi"]
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
    "Com esse sorriso, já nasceu sol no grupo. ☀️",
    "Se acordou com saudade, era eu nos teus sonhos. 💭",
    "Bom dia, princesa. Hoje o reino é só teu. 👑",
    "Teu bom dia vale mais que café forte. ☕",
    "Acorda, deusa. O Olimpo te espera. ✨",
    "Sol já nasceu, mas tua beleza ilumina mais. 🌞",
    "Bom dia, minha tentação favorita. 😈",
    "Nem precisa maquiagem: tua vibe já brilha. 💅",
    "Já pode parar de sonhar comigo e levantar. 😴❤️",
    "Bom dia, musa. Já desenhei teus lábios no pensamento. 💋",
    "Acordar sabendo que tu existe melhora meu humor. 🌸",
    "Bom dia com cheiro de ti. O resto é detalhe. 🌹",
    "Hoje acordei disposto a te admirar. 😍",
    "Bom dia, minha confusão preferida. 💫",
    "Tu é o tipo de caos que eu agradeço por ter. 🌀",
    "Tem gente que acorda. Tu... tu brota poesia. 📝",
    "Seus 'bom dia' deviam ser vendidos em cápsula de serotonina. 💊",
    "Acordou agora ou ainda tá sonhando comigo? 😜",
    "Bom dia, meu suspiro de todas as manhãs. 😮‍💨",
    "Dá bom dia pro sol, que hoje ele compete contigo. 🌞 vs 💁",
    "Bom dia, mulher que quebra minha pose de durão. 🫠",
    "Se beleza fosse despertador, tu me acordava todo dia. ⏰",
    "Desculpa sol, mas hoje ela é a única luz que eu preciso. 🌞💘",
    "Bom dia, charme ambulante. 🚶‍♀️✨",
    "Se meu bom dia chegou, é porque tu merece. 💌",
    "Tem gente que é café. Tu é o café, o pão, o banquete. 🍞☕",
    "Acorda devagar, tua presença já causa impacto. 💥",
    "Hoje é dia de sorrir. Tu já fez o meu. 😄",
    "Bom dia, emoção em forma de gente. ❤️",
    "Dormiu bem? Porque acordada tu tá impecável. 😍",
    "Deus caprichou demais nessa criatura que acordou agora. 🙏",
    "Tu tem cheiro de recomeço bom. 🌼",
    "Te ver online já faz meu dia começar direito. ✅",
    "Bom dia, mulher que me desconfigura. 🤯",
    "Tua vibe invade o grupo de um jeito gostoso. 😎",
    "Acorda e domina. O mundo já é teu. 🌍",
    "Acordou ou desceu direto do céu? ☁️",
    "Quem dera todo dia começasse com tua voz. 🎤",
    "Tu é o ‘acordei’ mais bonito que esse grupo já viu. 😘",
    "Bom dia, mistura perfeita de caos e calmaria. 🌪️🕊️",
    "Se for pra escolher um motivo pra sorrir cedo... é tu. 😊",
    "Seus stories já são meu café da manhã. 📱☕",
    "Com esse cabelo bagunçado, tu bagunça meu juízo. 😵",
    "Tu nasceu pra transformar dias comuns em mágicos. ✨",
    "Bom dia, mulher que me tira o ar e dá sentido. 💓",
    "Acorda, que hoje eu quero tua atenção. 🧲",
    "Só teu bom dia me faz ignorar todas as notificações. 🔕",
    "Tu é a notificação mais esperada do meu dia. 🔔❤️",
    "Nada contra o café, mas tu me acorda melhor. 😌",
    "Acorda que já tô com saudade. E tu nem saiu da cama ainda. 🛏️",
    "Tu é o tipo de presença que vale mais que mil mensagens. 💬💖",
    "Bom dia, sonho que virou vício. 💭➡️🔥",
    "Teu bom dia devia ter trilha sonora. 🎶",
    "Tu é o alarme que eu nunca ignoraria. 📲",
    "Acordou linda... de novo. Isso é perseguição? 😍",
    "Tua existência é o melhor bom dia do universo. 🌌",
    "Já começou o dia sendo arte, né? 🎨",
    "Se tu fosse sol, ninguém ia dormir mais. ☀️💛",
    "Só tu consegue dar um bom dia e hipnotizar junto. 👁️",
    "Se o céu tá limpo, é porque tu sorriu. 🌤️",
    "Nada supera tua energia matinal. Nem playlist animada. 🎵✨",
    "O grupo até fica mais leve quando tu aparece. 🪶",
    "Tu é a poesia da minha manhã. 📖💘",
    "Bom dia, paixão que eu disfarço mal. 🙈",
    "Tua existência já é bom dia o suficiente. 🙃",
    "Acorda, minha inspiração de todos os dias. ✏️❤️",
    "Tu acorda linda até sem filtro. Isso é feitiçaria? 🧙‍♀️",
    "O mundo gira melhor quando tu tá acordada. 🌍💫",
    "Só de saber que tu tá online, já fiquei mais animado. ⚡",
    "Bom dia, princesa do caos e da calmaria. 👑🔥"
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
        "ultima_repeticao": None
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

    # Xavecar mulher uma vez por dia
    if nome.lower() in [m.lower() for m in MULHERES]:
        ultima = historico["frases_mulheres_hoje"].get(str(usuario.id))
        if ultima != hoje:
            historico["frases_mulheres_hoje"][str(usuario.id)] = hoje
            salvar_historico()
            resposta = random.choice(xavecos_mulheres)
            bot.reply_to(msg, resposta)
            return

    # Debochar de homem uma vez por dia
    if nome.lower() in [h.lower() for h in HOMENS]:
        ultima = historico["respostas_homens_hoje"].get(str(usuario.id))
        if ultima != hoje:
            historico["respostas_homens_hoje"][str(usuario.id)] = hoje
            salvar_historico()
            resposta = random.choice(deboches_homens)
            bot.reply_to(msg, resposta)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
