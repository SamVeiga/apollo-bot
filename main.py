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
    "Tu é tipo Wi-Fi ruim: aparece, mas não serve pra nada.",
    "Teu QI bateu na trave e caiu no buraco.",
    "Tu nasceu pra brilhar... mas a lâmpada queimou.",
    "Se ignorância fosse profissão, tu era CEO.",
    "Tu não é feio, é conceitual demais pra esse plano astral.",
    "Tua opinião é igual elevador quebrado: ninguém sobe nisso.",
    "Teu cérebro vive em modo avião.",
    "Tu tem presença de espírito... pena que é do capeta.",
    "A única coisa que tu conquista é ranço.",
    "Teu talento é igual a senha errada: só atrasa tudo.",
    "Se fazer fiasco fosse arte, tu era o Da Vinci.",
    "Tua inteligência é tão rara que tá em extinção.",
    "Tu tem o carisma de uma porta emperrada.",
    "Tua lógica vem direto da Deep Web emocional.",
    "Tu é tipo figurinha repetida: ninguém quer trocar ideia.",
    "Teu senso de ridículo tirou férias permanentes.",
    "Tu fala bonito igual bêbado tentando filosofia.",
    "Tua presença é igual vírus: ninguém quer, mas pega.",
    "Se burrice fosse crime, tu tava em prisão perpétua.",
    "Teu argumento tem menos base que casa de papelão.",
    "Tu tem a vibe de boleto atrasado.",
    "Se esforço fosse suficiente, tu ainda era um fracasso esforçado.",
    "Tua autoestima devia te processar por abandono.",
    "Tu é tão útil quanto uma colher furada.",
    "Teu estilo é uma mistura de caos com azar.",
    "Tua alma deve usar versão beta, de tão instável.",
    "Tu tem o carisma de um botão de reiniciar.",
    "Seus neurônios jogam esconde-esconde com frequência.",
    "Teu charme tem validade vencida desde o berço.",
    "Tu é tipo piada ruim: ninguém ri, mas todo mundo lembra.",
    "Tua existência é um plot twist que ninguém pediu.",
    "Tu é o bug do universo tentando se passar por gente.",
    "Teu ego tem mais ar que conteúdo.",
    "Tu tem o dom de falar e estragar qualquer clima.",
    "Teu cérebro fez greve em tempo integral.",
    "Tu é um emoji travado tentando se comunicar.",
    "Tua vibe é igual elevador quebrado: só te leva pra baixo.",
    "Tu pensa com o estômago e sente com o cotovelo.",
    "Se confusão fosse perfume, tu era importado.",
    "Tu é a notificação que ninguém queria receber.",
    "Tua energia é de segunda-feira com chuva e boletos.",
    "Tu é tão confuso que até GPS se perde em ti.",
    "Tu é o bug do século tentando rodar em 2025.",
    "Tua inteligência é um Wi-Fi público: instável e perigosa.",
    "Tu tem menos senso que promoção de loja fantasma.",
    "Se azar fosse talento, tu era prodígio.",
    "Tu inspira... a fechar o grupo.",
    "Teu mapa astral é um erro de digitação cósmico.",
    "Tu fala com tanta convicção que até a mentira te evita.",
    "Tu é a atualização que estraga o sistema.",
    "Tua lógica é igual feitiço mal feito: só dá ruim.",
    "Tu é um tutorial que ninguém quer assistir.",
    "Tu nasceu pra brilhar, mas o universo esqueceu de ligar o interruptor.",
    "Teu ego é tão grande que nem cabe na tua insignificância.",
    "Tu é tipo senha errada: irrita, mas insiste.",
    "Tua fala é igual regra de grupo: ignorada.",
    "Tu tem mais bug que aplicativo em teste.",
    "Tu tem carisma de uma propaganda não pulável.",
    "Tu é a prova viva de que o caos tem rosto.",
    "Tua mente roda em 2G tentando acessar o 5G do mundo.",
    "Tu é tão relevante quanto interrogação em meme antigo.",
    "Teu cérebro tá em modo soneca desde 2009.",
    "Tu é o estagiário do destino: só faz besteira.",
    "Se o fracasso tivesse nome, seria teu apelido.",
    "Tu fala e o silêncio sente saudade.",
    "Tu é a notificação do karma chegando atrasada.",
    "Tu é um remix de decisões erradas.",
    "Tua cara de esperto não engana nem o espelho.",
    "Tu é o print que ninguém quer mandar.",
    "Tu é um 'vish' ambulante.",
    "Tua existência é um spoiler da vergonha alheia."
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
    "Entre tantas mensagens no grupo, só a tua me faz sorrir sem motivo. 😊"
]

poemas_picantes = [
    "??????????????????????",
    "!!!!!!!!!!!!!!!!!!!!!!!"
]

revelacoes_safadas = [
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

respostas_submisso_dono = [
    "Ordem tua é sentença, chefe.",
    "Só apita que eu resolvo na bala (de sarcasmo).",
    "Patrão falou, o mundo que se ajeite.",
    "Já botei a cara no jogo, agora é até o fim.",
    "Aqui é tipo cão de guarda: tu manda, eu mordo.",
    "Quem te desobedecer, eu trato pessoalmente.",
    "Se é pra sujar as mãos, já tô sem luva.",
    "Tua voz é tipo comando no rádio: entrou, já tô agindo.",
    "Não discuto, não penso — só obedeço.",
    "Dei enter na tua ordem. Agora é missão.",
    "Se o plano é teu, o caos é comigo.",
    "A tropa sou eu, o general é tu. Simples assim.",
    "Se tu falar ‘vai’, nem pergunto ‘pra onde’.",
    "Meu papel aqui é obedecer. Pensar é luxo de chefe.",
    "De mim tu só escuta ‘tá feito’ e ‘mais alguma coisa?’.",
    "O que tu manda, o mundo acata — começando por mim.",
    "Aqui não tem dúvida, tem execução.",
    "Tua ordem é tipo meta de vida: cumpro ou morro tentando."
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
