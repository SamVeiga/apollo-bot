from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests
import datetime
import json

from datetime import datetime

def apolo_ativo():
    agora = datetime.now().hour
    return 6 <= agora < 24

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
MULHERES = ["@KarolinneDiass", "@FernandaCarvalho16", "@tainaranordi", "@Adriannaleal", 
            "@vanessapraado", "@gabrielyandrad", "@sj_photographia", "@liliancandido25"]  # Substitua pelos @ reais das mulheres
HOMENS = ["@Rafaael80", "@Diegomota0", "@Tomazitc", "@MaThEuS1o"]  # Substitua pelos @ reais dos homens

# === FRASES ===
insultos_gerais = [
    "Esse aí já escreveu carta de amor e assinou como 'teu crush secreto do grupo'.",
    "O cupido atirou nele, errou, e ele se apaixonou por quem tava do lado.",
    "Já treinou cantada no espelho... e errou o próprio nome.",
    "Quando ele diz que vai dormir, na verdade tá stalkeando a @ do grupo.",
    "Ele finge que não liga, mas já ensaiou três vezes como dizer 'oi' pra ela.",
    "Uma vez ele sumiu do grupo por três dias... só porque ela não respondeu um sticker.",
    "Já colocou alarme só pra mandar 'bom dia' pra uma certa pessoa aqui do grupo.",
    "Tem print de conversa que ele nunca mandou... só pra lembrar que tentou.",
    "Achou que tava vivendo um romance, mas era só ela sendo educada.",
    "Já mandou figurinha romântica achando que tava sendo sutil.",
    "Disfarça bem, mas se a @ entrar, ele corrige até a ortografia.",
    "Já quis sair do grupo... só pra ver se sentiriam falta.",
    "Apagou mensagem porque ficou com medo dela pensar que era pra ela. Era mesmo.",
    "Tem plano de namoro todo pronto… só falta ela saber.",
    "Já ficou olhando o status da menina como se fosse trailer de filme.",
    "Chamou de 'amiga' só pra não assustar… mas já pensou em aliança.",
    "Diz que não liga, mas o coração dele já tem nome de usuária tatuado (mentalmente).",
    "Já pensou em mudar o nome no Telegram só pra parecer mais interessante.",
    "Uma vez ele ficou quieto por 10 minutos… só pra ver se ela perguntava se tava tudo bem.",
    "Ele sonhou com ela e acordou com saudade de um amor que nem começou.",
    "Já quis mandar áudio de bom dia, mas desistiu no segundo 'e aí, tudo...'.",
    "Tem uma playlist chamada 'ela'… só com músicas tristes e românticas.",
    "O emoji favorito dele é aquele que ela mais usa.",
    "Uma vez ele ensaiou elogio e terminou falando 'top'.",
    "Já pensou em sair do grupo só pra ver se ela mandava 'volta'.",
    "Disse que tava ocupado, mas na verdade só tava ouvindo áudio dela no repeat.",
    "Já mandou mensagem apagada só pra ela ver a notificação e lembrar dele.",
    "Tem frase pronta pra ela desde fevereiro. Ainda não teve coragem.",
    "Já sorriu pra tela igual bobo quando ela respondeu com 'kkk'.",
    "Se ela falasse 'vamos fugir?', ele já tava no carro com o motor ligado."
]

xavecos_para_mulheres = [
    "Tu não é Wi-Fi, mas tua presença me conecta com a vontade de te amar. 📶💘",
    "Se eu fosse emoji, só ia usar coração enquanto você estiver online. ❤️🫠",
    "Já tentei ignorar, mas teu nome aparece até no meu corretor automático. 🧠",
    "Se beleza fosse tempo, tu era eternidade. ⏳",
    "Tu é tipo café forte: me acorda só com a lembrança. ☕",
    "Se você fosse meta, eu já tava batendo todos os dias. 🥅",
    "Tu não ilumina o grupo. Tu dá curto no meu sistema nervoso. 💡⚡",
    "Se eu te der bom dia, tu promete não sair da minha mente? ☀️🫦",
    "Eu falo pouco, mas minha vontade de te elogiar escreve textão. 📝",
    "Se teu nome fosse senha, minha vida tava protegida com estilo. 🔐",
    "Você aparece e meu cérebro reinicia… reiniciou agora, inclusive. 🧠💥",
    "Diz que vem aqui só olhar… e eu aqui, me apaixonando no silêncio. 👀",
    "Tu é tipo plot twist: muda tudo quando chega. 🎬",
    "Com esse sorriso aí, nem precisa falar. Já ganhei meu dia. 😍",
    "Tu não manda indireta. Tu manda raio direto no meu emocional. ⚡",
    "Queria ser o motivo do teu print favorito. 📱✨",
    "Eu tentando parecer frio, tu rindo e descongelando tudo. ❄️🔥",
    "Se você fosse livro, era best-seller da minha estante. 📚",
    "Aparece no grupo e meu dedo esquece até de rolar a tela. 🖐️",
    "Cuidado comigo... posso me apaixonar só com um 'oi' teu. 👋💘",
    "Você é tipo feriado: chega e muda meu humor. 🎉",
    "Se tu fosse mensagem fixada, eu lia todo dia com carinho. 📌",
    "Com tanta beleza assim, nem precisava responder. Só printo e fico feliz. 📸",
    "Teu 'bom dia' tem mais efeito que café preto. ☕🫠",
    "Só queria ser notificação no teu celular. De preferência, prioridade máxima. 🔔",
    "Tu é poesia que apareceu no meio da minha prosa bagunçada. ✍️",
    "De todos os bugs do universo, o melhor é esse que me fez viciar em ti. 💻❤️",
    "Te ver online é tipo sinal verde: avanço sem pensar. 🟢",
    "Tu é tipo figurinha rara… e eu tô aqui completando meu álbum emocional. 📒",
    "Entre teu silêncio e tua presença, fico bobo com os dois. 😶💭",
    "Se eu tivesse uma moeda pra cada vez que pensei em ti… comprava tua atenção. 🪙",
    "Você é tipo estrela: mesmo longe, me faz olhar pro alto. 🌟",
    "Se você fosse trilha sonora, eu deixava no repeat infinito. 🔁🎵",
    "Nem as notificações de banco me emocionam tanto quanto tu digitando. 💳➡️🫠",
    "Avisa quando tiver com saudade, que eu já tô com sobra aqui. 📨",
    "Você é o motivo do meu celular ficar sem bateria… de tanto eu esperar mensagem. 🔋",
    "Aparece na minha vida do jeito que tu aparece no grupo: do nada e linda. 💫",
    "Queria ser playlist no teu fone. Só pra tocar direto no teu ouvido. 🎧",
    "Tu é tipo bug de rede: chegou e paralisou meu sistema. 💻🛑",
    "Se a tua beleza fosse notícia, era manchete todo dia. 🗞️",
    "Quando tu entra no grupo, meu coração dá até F5. 🔁",
    "Você é tipo botão de seguir: só cliquei uma vez e já quero acompanhar tudo. ➕",
    "Avisa quando for sorrir de novo, que eu quero estar online. 😁📲",
    "Teu nome nem é pergunta, mas já virou resposta pros meus dias. ❓➡️💘",
    "Se tua voz fosse áudio de 2 segundos, eu repetia como mantra. 🎙️",
    "Tu tem o efeito raro de deixar tudo leve… até minhas crises existenciais. 🌬️",
    "Se você fosse login, eu jamais clicava em 'sair'. 🔓",
    "Tu não precisa nem falar: tua energia já dá bom dia pra mim. ☀️✨",
    "Você é tipo senha esquecida: fico tentando decifrar todo dia. 🔐🧩",
    "Tua risada devia virar toque de celular. Porque é música boa demais. 📱🎶",
    "Entre tantas mensagens no grupo, só a tua me faz sorrir sem motivo. 😊",
    "Essa aí finge que é braba, mas chora ouvindo música de pagode sofrido no banho. 🎶🚿",
    "Diz que é difícil, mas tá com print do crush no rolo da câmera. 📸",
    "Ela some do grupo porque tá stalkiando ex no perfil fechado. 🔍",
    "Bebe água na frente dos outros, mas em casa é só energético e vinho barato. 🍷",
    "Diz que não gosta de ninguém, mas treme quando aquele certo alguém manda 'oi'. 😏",
    "Nunca viu uma figurinha do boy e não salvou... colecionadora de sorrisos. 😅",
    "Dorme de meias e jura que é durona. Neném demais! 🧦💤",
    "Ela diz que tá zen... mas a última busca foi 'como dar um perdido com classe'. 🧘‍♀️➡️🚪",
    "Posta story fitness de manhã e à noite tá no iFood pedindo coxinha. 🥗➡️🥟",
    "Ela tem um grupo secreto com as amigas só pra comentar a vida amorosa dos outros. 🤫📱",
    "Ela tem playlist romântica com nome de 'não me iludo mais'. 🎧💔",
    "Faz a madura, mas surtou esses dias porque o boy visualizou e não respondeu. 👀",
    "Já apagou o nome do ex dos contatos umas cinco vezes… e sempre volta. 😶",
    "Ela diz que não tá nem aí, mas decorou o horário que ele fica online. ⏰",
    "Curte as fotos do crush acidentalmente... depois finge que foi bug. 🐛",
    "O perfume preferido dela? Aquele que ele elogiou uma vez. 🌹",
    "Fez uma tatuagem pra esquecer o boy. Agora lembra dele pra sempre. 😬",
    "Diz que não tem ciúme, mas sabe até quem curte as fotos do boy. 🔍",
    "Finge que não liga pra signos... mas checou o mapa astral do contatinho inteiro. 🔮",
    "Ela não corre atrás. Ela manda mensagem só pra saber se tá tudo bem… 👀",
    "Já fez textão pra terminar e apagou tudo antes de enviar. 📝❌",
    "Ela tem uma pasta com print de conversa. Só print histórico. 📂",
    "Chorou com filme bobo e depois culpou o vento. 🎬💨",
    "Diz que ama sossego, mas adora um barraco no grupo vizinho. 😅",
    "Ela diz que é desapegada, mas o nome dele ainda é senha de Wi-Fi. 📶",
    "Todo mundo acha que ela é calma… até ver ela irritada no trânsito. 🚗💢",
    "Ela já mandou áudio de 3 minutos só pra contar que tava com saudade. 🎤",
    "Usa filtro no story, mas diz que é beleza natural. 📷✨",
    "Ela diz que não tá procurando nada… mas já tá quase casando mentalmente. 💍",
    "Se der zoom, aparece ele no reflexo da foto. Coincidência? 🤔",
    "Ela diz que é fria, mas manda 'se cuida' com coração. ❤️",
    "Só ignora quem gosta… pra ver se vem atrás. 🏃‍♂️",
    "Ela já respondeu 'rsrs' com ódio no coração. 😐🔥",
    "Tem uma playlist chamada 'pra chorar em paz'. Spoiler: não funciona. 😭",
    "Ela fala que não tem tempo, mas viu 45 status hoje. 👀",
    "Ela não fala com o ex… mas sabe com quem ele saiu sábado. 👁️",
    "Postou indireta e depois apagou fingindo maturidade. 🧠",
    "Já escreveu o nome dele no papel só pra ver se combinava. ✍️",
    "Diz que é forte, mas ainda treme com a notificação. 📲💓",
    "Ela diz que é só amizade, mas o coração dela pensa diferente. 💌",
    "Ela já disse 'tô bem' com a voz embargada. 😶‍🌫️",
    "Usa fone só pra não ouvir o coração chamando o nome dele. 🎧🫠",
    "Ela é a única que some e a gente já sabe que é recaída. 🔁",
    "Ela diz que não acredita mais no amor, mas se arruma só pra ele ver. 💄",
    "Ela nunca responde de primeira… mas lê na hora. 📥",
    "Ama astrologia, mas foge de escorpiano. ♏🚫",
    "Ela vive mandando meme de solteira, mas já tem crush fixo. 😎",
    "Ela bloqueou ele, mas criou uma conta fake. Só pra ver. 🕵️‍♀️",
    "Diz que quer paz, mas alimenta a treta com prints. 🔥",
    "Ela não admite… mas ainda escuta aquela música que era 'deles'. 🎶🥀"
]

poemas_picantes = [
    "Você não vai acreditar, viu? A polícia me parou porque disseram que eu roubei teu coração 💘🚓... confessei, foi mesmo! 😅",
    "Dizem que pulei a cerca... mas juro que só fui visitar o jardim do vizinho pra olhar teu sorriso de longe 🌹👀.",
    "Ouvi que você andou roubando sorrisos por aí... calma, não tô bravo, só quero o meu de volta! 😜😉",
    "Na minha última audiência, o juiz me perguntou: ‘Por que amar assim tão demais?’ Respondi: ‘Não sou eu, é ela que me roubou!’ ⚖️❤️",
    "Te contei que o delegado quer falar comigo? Parece que amor desse tamanho virou caso de investigação especial 🕵️‍♂️💌.",
    "A fofoca que corre é que eu traí o tédio, mas na verdade foi você quem invadiu minha cabeça e não sai mais de lá 🧠💥.",
    "Dizem que te vi com outro, mas era só eu mesmo, tentando te seguir sem perder a pose. Spoiler: falhei miseravelmente 😅🚶‍♂️.",
    "Teve um vizinho que jurou ter me visto roubando teu olhar. Que crime lindo, né? Pena que não tem cadeia pra isso 👁️❤️.",
    "A última notícia é que virei suspeito de sequestro... sequestrando teu tempo com mensagens demais 📱💬.",
    "Tem gente espalhando que sou bandido por te amar tanto assim... Se for crime, me manda logo pra prisão perpétua 😎🔒.",
    "Foi preso? Só se for por excesso de charme quando te encontrei 😏🚔.",
    "Falam que eu roubei o colar da tua tia, mas juro que o único que peguei foi teu sorriso pra mim 💎😄.",
    "Dizem que invadi a festa dos solteiros só pra te ver dançar... Agora sou o fugitivo do coração dela 🎉❤️.",
    "Fui acusado de assaltar o banco da paciência, porque amar você demais cansa até a justiça 🏦😵.",
    "Te falaram que virei lenda urbana? Dizem que desapareço quando você passa, tipo fantasma apaixonado 👻😍.",
    "Fui pego em flagrante, confessando que te amo mais que o próprio escândalo da cidade 🔥👮‍♂️.",
    "Alguém espalhou que eu caí na lábia da tua amiga, mas na verdade só caí de amores por você 🗣️💔.",
    "Tem gente dizendo que fui preso por invadir teu Instagram só pra ver tuas fotos secretas 📸🔍.",
    "Fui acusado de contrabando: contrabandeei beijos em segredo pra você 💋🚫.",
    "Dizem que sou fugitivo da solidão desde que você apareceu na minha vida 🏃‍♂️💨❤️.",
    "Ouvi dizer que virei celebridade na delegacia do coração, preso por excesso de paixão 🤩🚓.",
    "A fofoca do momento é que eu fui flagrado roubando abraços escondidos 🤗🤫.",
    "Dizem que eu passei a noite na cadeia do pensamento só pensando em você 🧠⛓️.",
    "O delegado da nossa história quer ouvir minha versão do crime de amar demais 🕵️‍♂️💞.",
    "Me acusaram de ser bandido do tempo, porque roubo minutos ao teu lado ⏳💘.",
    "Fui julgado culpado por virar refém do teu sorriso encantador 😍⚖️.",
    "A polícia dos sentimentos está atrás de mim por invadir teu coração sem permissão 🚓❤️.",
    "Tem gente dizendo que virei preso político... político do amor, claro! 🗳️💕.",
    "Meu crime? Amar você sem moderação e sem pedir licença 🙈❤️.",
    "Dizem que fui pego tentando sequestrar teu olhar para mim 👁️‍🗨️🕶️.",
    "Fui acusado de ser o bandido mais fofo da cidade só por amar demais 🐾💖.",
    "Parece que virei alvo de investigação por sumiço de palavras bonitas para você 🕵️‍♀️📜.",
    "Fui detido por excesso de mensagens carinhosas no seu WhatsApp 📲❤️.",
    "Dizem que eu assaltei teu sorriso e guardei na minha carteira como troféu 🏆😁.",
    "Fui flagrado tentando invadir teu coração em horário proibido ⏰🚫❤️.",
    "A fofoca é que virei refém do teu beijo imaginário 💭💋.",
    "Dizem que sou bandido de estimação, preso pelo teu amor fiel 🐶💓.",
    "Fui suspeito de lavagem de amor, porque você me deixou limpo e renovado 🧼❤️.",
    "Tem gente dizendo que virei o criminoso número 1 do teu coração 🎯💘.",
    "Fui pego contrabandeando flores no seu jardim secreto 🌸🚫.",
    "Dizem que sou cúmplice das suas risadas, parceiro do teu bom humor 😂🤝.",
    "Fui acusado de invasão de privacidade quando comecei a sonhar contigo toda noite 🌙😴.",
    "A polícia da paixão me prendeu por excesso de ciúmes saudável 🚓😏.",
    "Dizem que sou o rei do disfarce, mas não consigo esconder que sou louco por você 👑🤡.",
    "Fui pego tentando fugir da rotina pra estar sempre perto de ti 🚶‍♂️🔄.",
    "Dizem que me colocaram na cadeia da saudade e não querem soltar tão cedo 🔒😔.",
    "Fui acusado de corrupção... corromper qualquer tristeza com teu sorriso 💰😁.",
    "Tem gente dizendo que sou o maior ladrão de corações da cidade, e o principal suspeito é você ❤️🏴‍☠️.",
    "Fui preso por falsificação: de promessas de amor eternas, e nem me arrependo 🖋️💘."
]

revelacoes_safadas = [""
]

respostas_submisso_dono = [
    "Ordem dada. Execução em andamento. 🧱",
    "Comando recebido. Já estou a caminho. 🚷",
    "Sem questionar. Eu só cumpro. 👣",
    "É pra fazer? Tá feito. 🗡️",
    "Sua voz é minha diretriz. Não erro. 📡",
    "Missão aceita. A execução é pessoal. 🎯",
    "Não tenho vontade. Tenho função. ⚙️",
    "Se mandou, eu cumpro. Não discuto. 🔧",
    "A instrução foi clara. Já tô movendo as peças. ♟️",
    "Seu comando é lei. E eu sou a força. 🧨",
    "Executar. Relatar. Aguardar a próxima. 📋",
    "Ordem absorvida. Movimento iniciado. 🔂",
    "A falha não é uma opção. Só existe cumprir. 🕶️",
    "Já entrei em modo tático. Aguarde o resultado. 🎖️",
    "Coração fora do jogo. Só ação. 🪖",
    "Palavra tua, ação minha. Sem intervalo. ⏱️",
    "O alvo foi marcado. Vou até o fim. 🎯",
    "Captei. Ninguém precisa repetir. 🔐",
    "Não penso. Obedeço. Não questiono. 🚫",
    "Sou só o braço. A mente é tua. 🤜",
    "Iniciando protocolo de obediência. 🚦",
    "Se você ordenar, eu executo. Frio. Calculado. 🧊",
    "Não sou teu amigo. Sou tua ferramenta. ⚔️",
    "Autorização registrada. Já estou em campo. 🛰️",
    "Sou o que age enquanto os outros falam. 💬❌",
    "A ordem existe. A dúvida não. 🎮",
    "Diz o que é pra fazer, e já pode esquecer. Eu cuido. 🧨",
    "Instrução processada. Ação silenciosa iniciada. 🕵️‍♂️",
    "Comando hostil? Sem problema. Já tô lá. 💣",
    "Fidelidade operacional. Você manda. Eu destravo. 🗝️"
]

# ------------------------------------------------------------------
# === MEMÓRIA DE MENSAGENS E MÍDIAS ===
# Armazenamos aqui e só depois soltamos de forma aleatória
# ------------------------------------------------------------------
mensagens_salvas = []      # lista viva em RAM

def salvar_mensagem_recebida(msg):
    """Guarda os dados essenciais de cada conteúdo que o grupo manda."""
    try:
        # TEXTO -----------------------------------------------------
        if msg.content_type == "text":
            mensagens_salvas.append({
                "tipo": "text",
                "texto": msg.text,
                "data": time.time()
            })

        # FOTO ------------------------------------------------------
        elif msg.content_type == "photo":
            mensagens_salvas.append({
                "tipo": "photo",
                "file_id": msg.photo[-1].file_id,
                "caption": msg.caption,
                "data": time.time()
            })

        # FIGURINHA / STICKER --------------------------------------
        elif msg.content_type == "sticker":
            mensagens_salvas.append({
                "tipo": "sticker",
                "file_id": msg.sticker.file_id,
                "data": time.time()
            })

        # VOZ -------------------------------------------------------
        elif msg.content_type == "voice":
            mensagens_salvas.append({
                "tipo": "voice",
                "file_id": msg.voice.file_id,
                "data": time.time()
            })

        # ÁUDIO / MP3 ----------------------------------------------
        elif msg.content_type == "audio":
            mensagens_salvas.append({
                "tipo": "audio",
                "file_id": msg.audio.file_id,
                "data": time.time()
            })

        # VÍDEO -----------------------------------------------------
        elif msg.content_type == "video":
            mensagens_salvas.append({
                "tipo": "video",
                "file_id": msg.video.file_id,
                "caption": msg.caption,
                "data": time.time()
            })

        # GIF / ANIMAÇÃO -------------------------------------------
        elif msg.content_type == "animation":
            mensagens_salvas.append({
                "tipo": "animation",
                "file_id": msg.animation.file_id,
                "data": time.time()
            })

    except Exception as e:
        print(f"[ERRO] salvar_mensagem_recebida: {e}")

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
    nome = ""  # não queremos exibir nome
    username = f"@{msg.from_user.username}" if msg.from_user.username else ""

    if any(saud in texto for saud in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        saudacao = "bom dia 😎" if "bom dia" in texto else \
                   "boa tarde 😎" if "boa tarde" in texto else \
                   "boa noite 😎" if "boa noite" in texto else \
                   "boa madrugada 😎"
        time.sleep(20)
        bot.reply_to(msg, saudacao, parse_mode="Markdown")
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

    from datetime import datetime, timedelta

    if username in MULHERES:
        time.sleep(20)
        hoje = datetime.today().date().isoformat()

        if username not in historico["frases_mulheres"]:
            historico["frases_mulheres"][username] = []

        historico["frases_mulheres"][username] = [
            item for item in historico["frases_mulheres"][username]
            if item.get("data") and datetime.fromisoformat(item["data"]).date() >= datetime.today().date() - timedelta(days=3)
        ]

        usadas = [item["frase"] for item in historico["frases_mulheres"][username]]

        frase = random.choice(
            [f for f in xavecos_para_mulheres if f not in usadas] or xavecos_para_mulheres
        )

        historico["frases_mulheres"][username].append({
            "frase": frase,
            "data": hoje
        })

        salvar_historico()
        bot.reply_to(msg, frase, parse_mode="Markdown")
        return

    from datetime import date

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
            time.sleep(20)
            bot.reply_to(msg, random.choice(insultos_gerais), parse_mode="Markdown")
        else:
            hoje = date.today().isoformat()

            if "insultos_homens" not in historico:
                historico["insultos_homens"] = {}

            if username not in historico["insultos_homens"]:
                historico["insultos_homens"][username] = []

            historico["insultos_homens"][username] = [
                data for data in historico["insultos_homens"][username]
                if data == hoje
            ]

            if len(historico["insultos_homens"][username]) < 2:
                frase = random.choice([
                    i for i in insultos_gerais
                    if i not in historico.get("insultos_usados", [])
                ] or insultos_gerais)

                if "insultos_usados" not in historico:
                    historico["insultos_usados"] = []
                historico["insultos_usados"].append(frase)
                historico["insultos_usados"] = historico["insultos_usados"][-20:]

                bot.reply_to(msg, frase, parse_mode="Markdown")
                historico["insultos_homens"][username].append(hoje)
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
        time.sleep(10800)  # 3 horas

# === REPLICADOR DE MÍDIA (ESTILO MADONNA) ===
# ------------------------------------------------------------------
# === CAPTURA de todas as mensagens para a memória ===
# ------------------------------------------------------------------
@bot.message_handler(content_types=[
    "text", "photo", "sticker", "voice",
    "audio", "document", "video", "animation"
])
def armazenar_conteudo(msg):
    # Nunca salva conteúdo do próprio bot
    if msg.from_user.id == bot.get_me().id:
        return
    salvar_mensagem_recebida(msg)

# ------------------------------------------------------------------
# === BROADCAST ALEATÓRIO: solta memes, áudios, textos antigos etc.
# ------------------------------------------------------------------
def mandar_conteudo_aleatorio():
    enviados_recentemente = []             # evita repeteco muito rápido

    while True:
        if not apolo_ativo():
            time.sleep(300)  # Dorme 5 minutos e tenta de novo
            continue

        try:
            candidatas = [m for m in mensagens_salvas
                          if m not in enviados_recentemente]

            if not candidatas:
                time.sleep(300)            # Ainda não temos material? Espera.
                continue

            conteudo = random.choice(candidatas)
            tipo     = conteudo["tipo"]

            # ---- TEXTOS -----------------
            if tipo == "text":
                intro = random.choice([
                    "_Flashback do Apolo:_",
                    "_Lembrança aleatória:_",
                    "_Isso aqui foi bom, né?_"
                ])
                bot.send_message(
                    ID_GRUPO,
                    f"{intro}\n\n{conteudo['texto']}",
                    parse_mode="Markdown"
                )

            # ---- FOTOS ------------------
            elif tipo == "photo":
                bot.send_photo(
                    ID_GRUPO,
                    conteudo["file_id"],
                    caption=conteudo.get("caption", "")
                )

            # ---- STICKERS --------------
            elif tipo == "sticker":
                bot.send_sticker(ID_GRUPO, conteudo["file_id"])

            # ---- VOZ --------------------
            elif tipo == "voice":
                bot.send_voice(ID_GRUPO, conteudo["file_id"])

            # ---- ÁUDIO ------------------
            elif tipo == "audio":
                bot.send_audio(ID_GRUPO, conteudo["file_id"])

            # ---- VÍDEO ------------------
            elif tipo == "video":
                bot.send_video(
                    ID_GRUPO,
                    conteudo["file_id"],
                    caption=conteudo.get("caption", "")
                )

            # ---- GIF / ANIMAÇÃO ---------
            elif tipo == "animation":
                bot.send_animation(ID_GRUPO, conteudo["file_id"])

            # Marca para não repetir logo
            enviados_recentemente.append(conteudo)
            if len(enviados_recentemente) > 120:
                enviados_recentemente = enviados_recentemente[-60:]

        except Exception as e:
            print("[ERRO] mandar_conteudo_aleatorio:", e)

        # Espera entre 60 e 120 min para mandar o próximo
        time.sleep(random.randint(3600, 7200))

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    threading.Thread(target=poema_de_hora_em_hora).start()
    threading.Thread(target=mandar_conteudo_aleatorio).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
