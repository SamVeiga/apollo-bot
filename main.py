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
MULHERES = ["@KarolinneDiass", "@FernandaCarvalho16", "@tainaranordi", "@Adriannaleal", "@vanessapraado", "@gabrielyandrad"]  # Substitua pelos @ reais das mulheres
HOMENS = ["@Rafaael80", "@Diegomota0", "@Tomazitc"]  # Substitua pelos @ reais dos homens

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
    "Essa mulher tem olhar que derruba sistema de segurança.",
    "Essa mulher tem o tipo de beijo que te desliga do mundo por uns 3 dias.",
    "Dizem que ela já fez um segurança da balada pedir demissão por excesso de desejo.",
    "Essa aí não fala 'oi', ela dá bug no teu controle emocional.",
    "Ela já deixou um padre em crise existencial só com o olhar.",
    "Conhecida por apagar velas... com sopro e intenção.",
    "Essa garota já virou trend sem postar nada, só por existir.",
    "Uma vez ela deu bom dia... e três casais se separaram no mesmo dia.",
    "Já foi confundida com perfume, porque todo mundo queria sentir.",
    "Já deu nó em lençol de motel — com o próprio corpo.",
    "Ela tem mais histórias de motel que o Google Maps.",
    "Um gemido dela travaria até servidor da NASA.",
    "Já seduziu um motoboy só com a assinatura do Pix.",
    "Essa mulher já fez um boy chorar só com um áudio de 3 segundos.",
    "É tão quente que derrete gelo só de olhar.",
    "Já foi confundida com demônio: só aparece quando você tá fraco.",
    "O sutiã dela tem mais segredos que diário de adolescente.",
    "Já mandou mensagem errada de propósito só pra criar clima.",
    "Se ela te chama de 'bobo', prepara a alma: vem vício aí.",
    "Já virou lenda urbana em grupo de zap.",
    "Um beijo dela vem com 7 pecados embutidos.",
    "Já tirou a roupa só com palavras.",
    "Conhecida por transformar tímido em safado em menos de 5 mensagens.",
    "O que ela fez naquela escada de incêndio não cabe em poesia.",
    "Já fez até Alexa gemer sem querer.",
    "É a favor do desequilíbrio emocional com estilo.",
    "Essa não manda nude: ela manda vocação.",
    "Quando ela diz 'vem', o corpo obedece antes da mente.",
    "Se ela te responde com 'kkk', é porque tá te imaginando nu.",
    "Dizem que ela já deu choque... de tesão.",
    "Uma vez ela gemeu e o grupo caiu por conteúdo impróprio.",
    "Tem o dom de deixar gente casada com crise de fé.",
    "Uma mordida dela tem mais poder que senha de banco.",
    "Já causou AVC emocional com figurinha ousada.",
    "Quando ela some, alguém termina namoro.",
    "Já seduziu um pastor só com stories no espelho.",
    "Tem beijo que parece oração... e ela reza com a boca.",
    "Já fez o Wi-Fi cair de tanta energia sexual no ar.",
    "É a favor de relações sérias... entre quatro paredes e algemas.",
    "Já fez um ex voltar só com uma piscada.",
    "Uma vez ela soprou o pescoço de alguém e a alma saiu.",
    "Já assinou contratos com beijo e saliva.",
    "Quando ela chama de 'bichinho', a temperatura sobe em 5°C.",
    "É proibida em 3 estados por excesso de tentação.",
    "Uma piscada dela já quebrou noivado.",
    "Se ela some por 2 dias, tem gente que entra em abstinência.",
    "O toque dela já fez boy largar o vício do cigarro — e começar o dela.",
    "O corpo dela é censura 21+, a mente... nem Freud entendeu.",
    "Já deu beijo que fez a lua mudar de fase."
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
        username_bot = f"@{bot.get_me().username.lower()}"
        mencionou_bot = False

        # Verifica se houve menção com @
        if msg.entities:
            for entity in msg.entities:
                if entity.type == "mention":
                    texto_entidade = msg.text[entity.offset:entity.offset + entity.length]
                    if texto_entidade.lower() == username_bot:
                        mencionou_bot = True
                        break

        # Ou se escreveu o nome "apollo" (sem @), em qualquer lugar do texto
        if not mencionou_bot and "apollo" in msg.text.lower():
            mencionou_bot = True

        if mencionou_bot:
            time.sleep(20)
            bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")
        return

    if username in MULHERES:
        time.sleep(20)
        frase = random.choice(xavecos_para_mulheres)
        if username not in historico["frases_mulheres"]:
            historico["frases_mulheres"][username] = []
        revelacao = random.choice(
            [r for r in revelacoes_safadas if r not in historico["frases_mulheres"][username]]
            or revelacoes_safadas
        )
        historico["frases_mulheres"][username].append(revelacao)
        salvar_historico()
        bot.reply_to(msg, f"{nome}, {frase} {revelacao}", parse_mode="Markdown")
        return

from datetime import date, timedelta

# Função auxiliar para verificar se pode insultar hoje (máx 2x por dia)
def pode_insultar_hoje(usuario):
    hoje = date.today().isoformat()

    if "insultos_homens" not in historico:
        historico["insultos_homens"] = {}

    if usuario not in historico["insultos_homens"]:
        historico["insultos_homens"][usuario] = []

    # filtra só os registros do dia atual
    historico["insultos_homens"][usuario] = [
        data for data in historico["insultos_homens"][usuario]
        if data == hoje
    ]

    # permite até 2 insultos por dia
    return len(historico["insultos_homens"][usuario]) < 2

# Função para registrar insulto aplicado hoje para o usuário
def registrar_insulto(usuario):
    hoje = date.today().isoformat()
    historico["insultos_homens"][usuario].append(hoje)
    salvar_historico()


if username in HOMENS:
    username_bot = f"@{bot.get_me().username.lower()}"
    texto_minusculo = msg.text.lower()
    mencionou_bot = False

    if msg.entities:
        for entity in msg.entities:
            if entity.type == "mention":
                texto_entidade = msg.text[entity.offset:entity.offset + entity.length].lower()
                if texto_entidade == username_bot:
                    mencionou_bot = True
                    break

    if not mencionou_bot and "apollo" in texto_minusculo:
        mencionou_bot = True

    if mencionou_bot:
        # Responde insultando SEM limite se mencionou o bot
        time.sleep(20)
        bot.reply_to(msg, f"{nome}, {random.choice(insultos_gerais)}", parse_mode="Markdown")
    else:
        # Responde insultando no máximo 2x por dia se não mencionar
        if pode_insultar_hoje(username):
            frase = random.choice([
                i for i in insultos_gerais
                if i not in historico.get("insultos_usados", [])
            ] or insultos_gerais)

            if "insultos_usados" not in historico:
                historico["insultos_usados"] = []
            historico["insultos_usados"].append(frase)
            # mantém últimos 20 para evitar repetição próxima
            historico["insultos_usados"] = historico["insultos_usados"][-20:]

            bot.reply_to(msg, f"{nome}, {frase}", parse_mode="Markdown")
            registrar_insulto(username)

    salvar_historico()
    return

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
