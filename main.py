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
    "Tua presença muda o clima até de conversa fiada.",
    "Tu não fala, tu hipnotiza.",
    "Tua calma causa confusão no meu juízo.",
    "Seus passos escrevem poesia sem caneta.",
    "Tu é brisa que chega leve, mas vira furacão na mente.",
    "Tua risada altera até batimento cardíaco.",
    "Te olhar faz a lógica virar lembrança.",
    "Tua energia é perigo bom de sentir.",
    "Tu é mapa que confunde e guia ao mesmo tempo.",
    "Se tua pele fosse livro, eu lia sem ponto final.",
    "Teus olhos me fazem esquecer o caminho de volta.",
    "Se tu piscar devagar, eu perco a rota da sanidade.",
    "Tu é a vírgula entre meu juízo e meu desejo.",
    "Tu é silêncio barulhento que ecoa no corpo.",
    "Tua vibe é tipo imã pra pensamento torto.",
    "Se for sonho, que demore pra acordar.",
    "Tua presença tem gosto de coisa rara.",
    "Tu é pausa que acelera tudo por dentro.",
    "Você me bagunça com um sorriso quieto.",
    "Teu cheiro parece lembrança que nunca aconteceu.",
    "Tua ausência dói menos que tua presença intensa.",
    "Tu fala com o olhar e ninguém te traduz.",
    "Tu passa devagar, mas deixa rastro eterno.",
    "Seus gestos são pista de fuga do juízo.",
    "Tu não entra em lugar, tu muda o ambiente.",
    "Tua calma acende incêndio interno.",
    "Tu não flerta, tu faz quem olha tropeçar no próprio pensamento.",
    "Se olhar fosse abraço, o teu já me envolveu.",
    "Teu jeito tem ritmo de música boa sem refrão.",
    "Tu é aquela mensagem não enviada, mas que o corpo entende.",
    "Você é o caos mais bonito que eu já quis viver em silêncio.",
    "Tu tem presença que não precisa de som pra fazer barulho.",
    "Tua ausência incomoda menos que tua lembrança.",
    "Se tu for vício, tô sem força pra largar.",
    "Tua risada abre porta onde não tem parede.",
    "Te olhar é correr risco com gosto.",
    "Tu é gatilho que dispara o inesperado.",
    "Teu andar tem trilha sonora própria.",
    "Tu tem jeito de quem chegou pra bagunçar a rotina.",
    "Se tu for céu, eu quero voar sem paraquedas.",
    "Tua leveza pesa em mim de um jeito bom.",
    "Teu silêncio tem mais efeito que grito.",
    "Tu entra na mente como quem já conhece o caminho.",
    "Você é pausa na correria que vira vício.",
    "Tu é a curva que meu juízo não faz.",
    "Se for pra me perder, que seja no teu olhar quieto.",
    "Tua sombra já muda a cor da minha vontade.",
    "Você é desejo vestido de calma.",
    "Teu toque imaginado já bagunça os sentidos.",
    "Tu é o detalhe que vira tempestade.",
    "Você é tipo saudade sem data.",
    "Se o tempo parar perto de ti, eu não reclamo.",
    "Teu cheiro tem assinatura de lembrança eterna.",
    "Tu é rastro em pensamento descalço.",
    "Tua presença desliga meu filtro racional.",
    "Você sorri e muda o sabor do instante.",
    "Tua voz ecoa mesmo em silêncio.",
    "Tu é o tipo de distração que vicia.",
    "Teu olhar tem tom de promessa.",
    "Tua leveza desarma qualquer escudo.",
    "Tu passa e o mundo desacelera.",
    "Se tua pele tivesse estação, seria verão infinito.",
    "Você é pretexto de pensamento constante.",
    "Teus gestos parecem dança escrita com vento.",
    "Tua alma brilha em baixa luz.",
    "Tu acende vontade só com presença.",
    "Te olhar de longe já bagunça meu eixo.",
    "Você é calma que inquieta.",
    "Teu nome soa como sussurro bom na alma.",
    "Tu tem presença de final feliz.",
    "Teu silêncio tem trilha sonora interna.",
    "Você é provocação que não precisa palavras.",
    "Teus olhos confundem o que é certo.",
    "Tua leveza arrasta o que parecia firme.",
    "Você é poesia que ninguém ousa declamar.",
    "Tua ausência é barulho na mente.",
    "Teus gestos traduzem vontades escondidas.",
    "Você é tipo alerta bonito do universo.",
    "Tua vibe é luar no meio do caos.",
    "Tu é a contradição que vale a pena.",
    "Tua presença tem cheiro de liberdade quente.",
    "Você é refúgio que bagunça.",
    "Tu é calmaria que chama tempestade.",
    "Teus passos ativam imaginação desgovernada.",
    "Você é pausa no mundo em modo rápido.",
    "Tua pele tem memória de desejo bom.",
    "Tu é farol em estrada confusa.",
    "Tua sombra muda o tom do dia.",
    "Você é aquele ponto de interrogação que eu nunca quis responder.",
    "Teu olhar tem gosto de fim que começa.",
    "Tu é pausa que parece fim de mundo.",
    "Você é pergunta que o corpo responde com silêncio.",
    "Tua leveza pesa no pensamento.",
    "Tu tem voz que desenha labirinto.",
    "Você é caminho de volta sem mapa.",
    "Tua calma grita no meu peito.",
    "Você é tipo nota musical escondida em silêncio.",
    "Tua presença reescreve o ambiente.",
    "Tu é memória que ainda nem aconteceu.",
    "Você tem gosto de risco bom.",
    "Tua energia é tempestade embalada em calma.",
    "Você é o detalhe que vira obsessão.",
    "Tu é a vírgula que muda o sentido do meu dia.",
    "Tua existência é trilha que meu pensamento percorre sem fim."
]

poemas_picantes = [
    "Te encontro no silêncio das intenções e te beijo com o olhar antes da pele.",
    "Tem coisa em você que arrepia o que nem devia sentir.",
    "Quando tua boca cala, tua presença grita tudo o que quero ouvir no escuro.",
    "Entre um toque e um suspiro teu, eu me perco no que não sei dizer em voz alta.",
    "Se teu cheiro já confunde minha alma, imagina tua presença inteira no meu espaço.",
    "Teus olhos têm a coragem que minha boca ainda não teve contigo.",
    "O que tua pele provoca, nem o tempo consegue apagar.",
    "Meu desejo mora nos detalhes que ninguém vê em ti, mas eu já decorei.",
    "Tem abraço teu que parece promessa... daquelas que a gente não quer que acabe.",
    "Te ter por perto é o mesmo que deixar o instinto abrir as portas do controle.",
    "Você é o tipo de silêncio que meu corpo entende como convite.",
    "Quando tua risada encosta em mim, meu juízo tira folga.",
    "Tua presença tem gosto de segredo contado no pé do ouvido.",
    "Te olhar é como ouvir um sussurro que só minha pele entende.",
    "Cada vez que tu me encara, um pedaço do mundo perde o sentido.",
    "Você tem cheiro de coisa boa... daquelas que viciam e ninguém conta pra mãe.",
    "Se eu me aproximar demais, prometo só encostar... mas com o coração inteiro.",
    "Teu toque é rastro, teu olhar é aviso, e teu silêncio... convite.",
    "No teu abraço mora o caos mais bonito que eu já quis repetir.",
    "Tem parte de mim que só acorda quando você chega perto.",
    "Você tem a intensidade de um pôr do sol visto da pele, não dos olhos.",
    "Te ver de longe já me toca em lugares que nem o vento alcança.",
    "Seus gestos me fazem poesia antes mesmo do primeiro beijo.",
    "Na tua presença, até o tempo se embriaga e perde a linha.",
    "O jeito que tu existe me bagunça como só os sonhos mais perigosos fazem.",
    "Quando teu nome entra na minha cabeça, o resto do mundo sai.",
    "Tu é aquele risco que eu correria devagar, só pra aproveitar o caminho.",
    "Seus olhos acendem em mim vontades que eu nem sabia que existiam.",
    "Tu me desarma com o silêncio e me domina com um sorriso torto.",
    "Te desejo na velocidade que a alma aceita sem avisar o juízo.",
    "Tua voz tem tom de promessa feita com as mãos nas costas.",
    "Quando teu perfume me encontra, minha calma tira férias.",
    "Você me causa um arrepio que nem a razão explica... mas o corpo sente.",
    "Tem coisa em ti que bate mais forte que saudade, e mais doce que vício.",
    "Se teu toque fosse música, seria trilha sonora de arrepios.",
    "Tua ausência me provoca, mas tua presença me consome inteiro.",
    "Você é o tipo de acaso que o destino escreve em braile na pele.",
    "Seus gestos falam com a minha vontade como se já soubessem meu endereço.",
    "Tem desejo teu que eu carrego no peito como quem guarda segredo no bolso.",
    "Com você, até o silêncio parece barulho de intenção.",
    "Tua presença tem gosto de coisa errada feita com alma limpa.",
    "Te quero perto como se distância fosse ofensa.",
    "Você tem cheiro de poesia que acabou de ser escrita com a ponta dos dedos.",
    "Cada passo teu em minha direção já é um toque sem encostar.",
    "Você é labirinto e atalho ao mesmo tempo — me perco e me acho no mesmo segundo.",
    "Teus gestos falam baixo, mas meu corpo escuta alto.",
    "Se tua presença fosse crime, eu confessava sem nem ser interrogado.",
    "No teu olhar mora um mistério que eu quero desvendar por dentro.",
    "Tem noite que só faria sentido com tua respiração na minha nuca.",
    "Você é tempestade calma: entra sem pressa, mas vira tudo de cabeça pra baixo.",
    "Me arrepio só de lembrar do que ainda nem aconteceu entre nós.",
    "Teu jeito é verso proibido em poema que ninguém ousou escrever.",
    "Tu é presença que ocupa espaço até quando se afasta.",
    "Quando teu nome aparece, meu corpo responde antes do pensamento.",
    "Te quero com o cuidado de quem sabe o que um toque pode fazer com a alma.",
    "Você é o intervalo entre um controle e uma rendição que nunca termina.",
    "Tua boca tem mais promessas do que qualquer palavra que eu conheço.",
    "Quando me olha daquele jeito, parece que lê meus segredos mais íntimos.",
    "Você tem cara de perigo e alma de abrigo... tudo ao mesmo tempo.",
    "Te desejo como quem implora por um segundo a mais num sonho bom.",
    "Teu silêncio me diz mais do que mil mensagens ousadas.",
    "Na tua presença, até minha respiração muda de tom.",
    "Se tua pele fosse mapa, eu me perderia só pra ter que explorar tudo de novo.",
    "Você é vontade que não passa, mesmo depois que fecho os olhos.",
    "Te encontro em pensamentos onde nem o sono ousa ir.",
    "Tua presença me faz esquecer que o mundo gira... porque você já me vira do avesso.",
    "Tu é desejo calmo, daqueles que não gritam — mas dominam.",
    "Com você, até o toque mais leve parece poesia tatuada na alma.",
    "Se teus beijos fossem caminho, eu andava de olhos vendados.",
    "Você tem um quê de proibido... que desperta tudo o que é permitido só entre dois corpos em silêncio."
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
    "Já deu beijo que fez a lua mudar de fase.",
    "Ela não entra em grupo... ela muda o clima.",
    "Ela já fez um boy escrever textão sem nem responder 'oi'.",
    "Tem figurinha dela que virou fetiche coletivo.",
    "Só o áudio dela rindo já serve de provocação proibida.",
    "Já foi motivo de terapia... e de recaída também.",
    "Ela usa emoji como se fossem feitiços sexuais.",
    "Tem sorriso que parece filtro de safadeza ativado.",
    "Já deixou boy gaguejando com só uma foto de costas.",
    "Ela dá bom dia como quem abre porta de motel.",
    "Tem figurinha dela circulando em grupo secreto.",
    "Só a sombra dela já dá calor em chat frio.",
    "Já deu bloqueio mental em quem jurava ser racional.",
    "Ela tem foto que faz o Wi-Fi cair só de tentar abrir.",
    "Foi banida de grupo porque mandou só um 'oi'.",
    "Ela ativa gatilho até em quem dizia ser frio.",
    "Já causou crise em namoro só com legenda ambígua.",
    "Tem olhada que parece trilha sonora de pornô francês.",
    "Ela tem presença que parece spoiler de noite quente.",
    "Seus áudios já foram usados como despertador de fetiche.",
    "Ela inspira gemido só com stories.",
    "Tem nome salvo como 'perigo' e ninguém muda.",
    "Ela não precisa falar besteira: o silêncio já é explícito.",
    "Já tirou o sono de gente que só viu a bio.",
    "Ela tem foto que dá sede... e não é de água.",
    "Um 'oi' dela já fez o boy pensar em mudar de país com ela.",
    "Já causou conflito interno em crente convicto.",
    "O emoji preferido dela é aquele que ninguém deveria usar no trabalho.",
    "Tem jeito de calma, mas causa caos hormonal.",
    "Ela fez um ADM sair do grupo só pra não cair em tentação.",
    "Já fez dublagem de gemido virar ringtone alheio.",
    "Tem gif dela que circula como lenda urbana nos grupos.",
    "Ela já fez uma DR só com reação de emoji.",
    "Só o print de conversa com ela já ferve galeria.",
    "Ela tem a pose de quem sabe o que fazer com a língua.",
    "O status dela já serviu de indireta pra quatro ex.",
    "Tem vídeo dela parado que parece trailer proibido.",
    "Só a respiração dela num áudio causou abstinência.",
    "Já teve figurinha censurada por indecência emocional.",
    "Ela posta meme e o povo interpreta como convite.",
    "Já foi confundida com IA: perfeita e fora da realidade.",
    "Ela olha como quem já sabe onde vai te morder.",
    "Foi marcada em oração por motivo de tentação.",
    "Ela tem selfie que deveria vir com aviso de 'NSFW'.",
    "Já recebeu elogio que mais parecia pedido de socorro.",
    "Ela já causou briga em grupo que ela nem participava.",
    "Ela é o tipo de print que se compartilha em silêncio.",
    "Já fizeram análise de texto só pra entender o 'oi' dela.",
    "Já tirou o fôlego de quem só viu o @ aparecendo na notificação.",
    "Ela dá tchau com emoji e deixa a mente presa por 3 dias.",
    "Tem gente que já pegou ranço de quem curte as fotos dela demais.",
    "Ela faz story de comida parecer prévia de motel.",
    "Já confundiu até chatbot com mensagem ousada.",
    "Ela tem vídeo de 3 segundos que parece cena de filme 18+.",
    "É mencionada em sonhos e apagada da consciência por segurança.",
    "Ela some por 1 dia e a libido coletiva entra em pânico.",
    "Ela já deu um sorriso que virou motivo de recaída nacional.",
    "O nome dela na conversa já vem com emoji de alerta.",
    "Tem dublagem dela em figurinha que ninguém tem coragem de abrir no trabalho."
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

        # Resposta especial para mulheres
    id_unico = msg.from_user.username if msg.from_user.username else str(msg.from_user.id)
    if id_unico in MULHERES:
        hoje = datetime.date.today().isoformat()
        if "respostas_mulheres" not in historico:
            historico["respostas_mulheres"] = {}
        if id_unico not in historico["respostas_mulheres"]:
            historico["respostas_mulheres"][id_unico] = []

        # Remove respostas antigas
        historico["respostas_mulheres"][id_unico] = [
            data for data in historico["respostas_mulheres"][id_unico] if data == hoje
        ]

        username_bot = f"@{bot.get_me().username.lower()}"
        mencionou_bot = False

        if msg.entities:
            for entity in msg.entities:
                if entity.type == "mention":
                    texto_entidade = msg.text[entity.offset:entity.offset + entity.length]
                    if texto_entidade.lower() == username_bot:
                        mencionou_bot = True
                        break

        if not mencionou_bot and "apollo" in msg.text.lower():
            mencionou_bot = True

        # Se mencionou, ou se ainda pode responder hoje
        if mencionou_bot or len(historico["respostas_mulheres"][id_unico]) < 2:
            frase = random.choice(xavecos_para_mulheres)
            if id_unico not in historico["frases_mulheres"]:
                historico["frases_mulheres"][id_unico] = []
            revelacao = random.choice(
                [r for r in revelacoes_safadas if r not in historico["frases_mulheres"][id_unico]]
                or revelacoes_safadas
            )
            historico["frases_mulheres"][id_unico].append(revelacao)
            historico["respostas_mulheres"][id_unico].append(hoje)
            salvar_historico()
            time.sleep(20)
            bot.reply_to(msg, f"{nome}, {frase} {revelacao}", parse_mode="Markdown")
            return

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
