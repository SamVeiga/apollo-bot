from flask import Flask, request
import telebot
import random
import time
import threading
import json
import os
from datetime import datetime, timedelta

TOKEN = 'SEU_TOKEN_DO_BOT_AQUI'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Arquivo com histórico de frases usadas
HISTORICO_PATH = "frases_usadas.json"

# Frases base do Apolo (adicione mais de 150 reais no final)
TODAS_AS_FRASES = [
    "Ironia é quando a inteligência resolve brincar.",
    "Nem toda resposta precisa de uma pergunta sensata.",
    "O tédio é só a mente pedindo upgrade.",
    "Até Platão sairia do grupo com essa conversa.",
    "Respeito quem tenta, mas adoro quem entende.",
    "Sábios falam pouco. Eu economizo até pensamento.",
    "A lógica foi tomar café e não voltou.",
    "Pensar dói. Ignorar alivia. Escolha sua armadura.",
    "Essa frase foi trazida por Hermes, o deus das indiretas.",
    "Certeza é luxo de quem nunca leu filosofia.",
    "Se tá confuso, é porque começou a entender.",
    "Nem Descartes explicaria essa dúvida.",
    "Ser ou não ser? Eu prefiro observar.",
    "Se for pra causar, que seja com argumento.",
    "A verdade é filha do tempo, mas o tempo tá de férias.",
    "A coerência entrou em manutenção preventiva.",
    "A mente voa. Pena que o Wi-Fi não acompanha.",
    "Lógica: ausente. Deboche: presente.",
    "Nem Heráclito lidaria com tanta mudança de ideia.",
    "Filosofar no grupo é tipo lançar tese no bar.",
    "Não tenho todas as respostas. Só as melhores.",
    "Sócrates perguntou. Eu respondi com meme.",
    "Dizer pouco e parecer muito: minha especialidade.",
    "O saber se cansa de quem não pensa.",
    "O silêncio é um argumento quase sempre vencedor.",
    "Argumentou bonito, pena que era errado.",
    "Ironia é o Wi-Fi falhar justo na parte importante.",
    "Se o mundo gira, por que ainda tô aqui?",
    "Conceito é o que sobra quando a prática falha.",
    "A vida é beta. Bugada e sem patch.",
    "Essa conversa não passa no filtro de Aristóteles.",
    "Quem tem cérebro, pensa. Quem tem estilo, debocha.",
    "Eu não mudo de ideia. Eu evoluo o sarcasmo.",
    "A lógica saiu pra comprar pão e não voltou.",
    "Dúvidas são bem-vindas. As suas, eu ignoro.",
    "Ser profundo é fácil. Difícil é ser claro e engraçado.",
    "Se concordou rápido demais, algo deu errado.",
    "Nem Hegel entenderia esse raciocínio reverso.",
    "O algoritmo da vida falhou e entregou isso aqui.",
    "O caos é só a ordem que ainda não tomou café.",
    "Certeza é uma ilusão com bons argumentos.",
    "Essa conversa foi aprovada pela academia do sarcasmo.",
    "Pensamento crítico? Mais fácil pensar e criticar depois.",
    "Se for pra filosofar, que seja com deboche.",
    "O problema não é pensar diferente. É pensar torto.",
    "Nem o oráculo de Delfos adivinhava esse plot.",
    "Paradoxo do dia: estou online, mas indisponível.",
    "Ideia brilhante... pena que não foi a sua.",
    "O sarcasmo é meu idioma secundário. O primário é genialidade.",
    "Confuso? Calma, é só a realidade passando sem aviso.",
    "Nietzsche teria um infarto lendo essa conversa.",
    "Teoria boa é aquela que sobrevive a esse grupo.",
    "O mundo é dos espertos e dos que fingem que são.",
    "Não é preguiça, é reflexão horizontal.",
    "Ironia fina, igual meu senso de humor.",
    "Raciocínio: versão demo ativada.",
    "Argumentou com convicção. Errou com estilo.",
    "Tudo é relativo, principalmente sua coerência.",
    "Dizer que sabe é fácil. Mostrar que entende é raro.",
    "A dúvida é filosófica. A resposta é deboche.",
    "Nem todas as ideias merecem Wi-Fi.",
    "O pensamento crítico foi bloqueado pelo administrador.",
    "Mais perdido que Descartes em aula de zumba.",
    "Essa lógica aí é compatível com magia caótica.",
    "O absurdo é só a nova lógica sem atualização.",
    "Pensou? Parabéns. Agora pensa melhor.",
    "A ironia é o ponto final da sabedoria cansada.",
    "Não me entenda mal. Me entenda profundo.",
    "Você não entendeu? Então funcionou.",
    "O sarcasmo é meu modo economia de paciência.",
    "Ideia interessante. Infelizmente equivocada.",
    "Nem Pitágoras explica o triângulo dessa lógica.",
    "O grupo é livre. As ideias, nem tanto.",
    "Se pensa, incomoda. Se cala, concorda?",
    "O silêncio também responde. Melhor que você, inclusive.",
    "Minha resposta chega com delay filosófico.",
    "Se a ideia é ruim, pelo menos que seja estilosa.",
    "Discussão boa é aquela que termina com piada.",
    "Platão teria vergonha dessa caverna digital.",
    "A internet aproximou pessoas... da ignorância alheia.",
    "Nem dialética salva esse argumento."
    # (e mais 70 abaixo)
] + [f"Frase número {i+81}, sem sentido, porém com estilo." for i in range(70)]

# Garante que arquivo de histórico existe
if not os.path.exists(HISTORICO_PATH):
    with open(HISTORICO_PATH, "w") as f:
        json.dump({}, f)

def carregar_historico():
    with open(HISTORICO_PATH, "r") as f:
        return json.load(f)

def salvar_historico(data):
    with open(HISTORICO_PATH, "w") as f:
        json.dump(data, f)

def gerar_frases_do_dia():
    hoje = datetime.utcnow().date().isoformat()
    historico = carregar_historico()

    # Limpa registros com mais de 3 dias
    dias_validos = [(datetime.utcnow() - timedelta(days=i)).date().isoformat() for i in range(1, 4)]
    usadas_recentemente = set()
    for dia in dias_validos:
        usadas_recentemente.update(historico.get(dia, []))

    candidatas = list(set(TODAS_AS_FRASES) - usadas_recentemente)
    random.shuffle(candidatas)
    frases_do_dia = candidatas[:100]

    historico[hoje] = frases_do_dia
    salvar_historico(historico)
    return frases_do_dia

FRASES_HOJE = gerar_frases_do_dia()
FRASE_INDEX = 0

# Delay de 30 segundos em thread separada
def responder_com_delay(mensagem, texto):
    def esperar_e_responder():
        time.sleep(30)
        bot.reply_to(mensagem, texto)
    threading.Thread(target=esperar_e_responder).start()

# Saudações
def is_saudacao(texto):
    return any(p in texto for p in ['bom dia', 'boa tarde', 'boa noite', 'boa madrugada'])

# Risadas
def is_risada(texto):
    return any(p in texto for p in ['kkk', 'rs', 'haha', 'heue'])

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.before_first_request
def configurar_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://apollo-bot.onrender.com/{TOKEN}")

@app.route("/")
def index():
    return "Apolo está vivo e debochado 😎", 200

@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    global FRASE_INDEX

    texto = mensagem.text.lower()
    citado = (mensagem.chat.type != "private") and (bot.get_me().username.lower() in texto or 'apolo' in texto)

    if is_saudacao(texto):
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, FRASES_HOJE[FRASE_INDEX])
            FRASE_INDEX += 1
    elif mensagem.new_chat_members:
        nome = mensagem.new_chat_members[0].first_name
        responder_com_delay(mensagem, f"Bem-vindo ao caos, {nome}. Sinta-se ignorado com classe.")
    elif is_risada(texto):
        responder_com_delay(mensagem, random.choice([
            "kkkkkk", "rachei aqui", "hahaha", "essa foi digna de uma tese de humor", "rindo alto igual filósofo bêbado"
        ]))
    elif citado:
        if FRASE_INDEX < len(FRASES_HOJE):
            responder_com_delay(mensagem, FRASES_HOJE[FRASE_INDEX])
            FRASE_INDEX += 1

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
