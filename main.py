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
    "Se você fosse um livro, eu relia cada página só pra te ter mais uma vez.",
    "Você é tipo Wi-Fi bom: me conecta, me acalma e me deixa viciado.",
    "Nem o ChatGPT consegue simular a perfeição que você é.",
    "Você não é paisagem, mas me deixa sem palavras toda vez que aparece.",
    "Seu sorriso é meu atalho pra felicidade.",
    "Se você fosse um sonho, eu dormia pra sempre.",
    "Você tem um jeito de mexer comigo que nem o vento consegue.",
    "Seu olhar vale mais que qualquer poesia.",
    "Você é aquela vírgula no meu caos... que eu quero em ponto final.",
    "Se o coração tivesse playlist, o seu seria faixa principal.",
    "Você tem cheiro de tudo que dá certo.",
    "Se amar fosse profissão, eu trabalhava em tempo integral por você.",
    "Você tem mais encanto que lua cheia refletida no mar.",
    "Você não anda, você desfila dentro da minha cabeça.",
    "Nem dicionário explica o que sinto quando te vejo.",
    "Você é aquela notificação que eu nunca colocaria no silencioso.",
    "Se você fosse app, eu assinava vitalício.",
    "Com você por perto, até segunda-feira fica gostosa.",
    "Você é o tipo de calmaria que o mundo precisa.",
    "Seus olhos têm GPS: me perco fácil neles.",
    "Se for pra cair... que seja no seu sorriso.",
    "Você é o bug mais bonito do meu sistema emocional.",
    "Você é um plot twist que eu quero viver todo dia.",
    "Você tem o poder de transformar qualquer momento comum em poesia.",
    "Se for pra ser clichê, que seja com você.",
    "Você é minha variável favorita nesse código confuso da vida.",
    "Nem filtro melhora o que você já é.",
    "Se você fosse uma música, estaria no repeat eterno.",
    "Você é meu favorito mesmo quando o mundo tá em modo aleatório.",
    "Te ver é tipo café forte: acelera e acalma ao mesmo tempo.",
    "Você tem o charme de uma vírgula no meio de um parágrafo perfeito.",
    "Se teu sorriso fosse figurinha, eu usava até travar o WhatsApp.",
    "Você me deixa no modo avião... voando só por pensar em você.",
    "Se você tivesse um botão, seria 'encantar'.",
    "Você é o tipo de conexão que não precisa de senha.",
    "Com você, o tempo desacelera e o mundo faz mais sentido.",
    "Você tem luz própria e ainda ilumina os meus pensamentos.",
    "Se eu fosse poeta, você era meu verso favorito.",
    "Você é tipo sol em inverno: chega devagar, aquece sem pressa.",
    "Seu jeito me desmonta com classe.",
    "Você é ponto de exclamação no meu dia comum.",
    "Se você fosse rede social, eu curtia até pensamento antigo.",
    "Você tem uma vibe que nem sábado à noite consegue competir.",
    "Não sei se é amor... mas quando te vejo, meu mundo dá um refresh.",
    "Você me deixa em modo 'salvar nos favoritos'.",
    "Você não é perfume, mas deixou teu cheiro em tudo aqui.",
    "Se você fosse menu, eu clicava em 'amar' sem pensar.",
    "Você tem mais presença que aviso de bateria fraca.",
    "Com você, tudo parece teaser de filme bom.",
    "Você tem aquele tipo de beleza que não dá pra dar print.",
    "Até o silêncio com você tem som de abraço.",
    "Você é mais bonita que a notificação de 'foi depositado'.",
    "Tua presença vale mais que Wi-Fi grátis.",
    "Você é aquele detalhe que muda tudo.",
    "Você é a legenda perfeita pra todas as minhas vontades.",
    "Se tua risada fosse trilha sonora, eu escutava todo dia.",
    "Você tem mais carisma que final feliz de novela.",
    "Se eu fosse emoji, seria coração só pra viver grudado contigo.",
    "Você é o tipo de mensagem que eu nunca colocaria em arquivar.",
    "Te olhar é tipo trailer: dá vontade de ver mais.",
    "Você é aquela coincidência que parece destino.",
    "Se você fosse mapa, eu me perderia de propósito.",
    "Você é a senha do meu bom humor.",
    "Com você, até segunda-feira tem gosto de sexta.",
    "Seu sorriso tem poder de rebootar meu dia inteiro.",
    "Você é tipo sonho que eu nem tento acordar.",
    "Tua beleza é tipo spoiler de coisa boa.",
    "Você não precisa de legenda... teu olhar já diz tudo.",
    "Se teu abraço fosse aplicativo, tava em primeiro lugar no ranking.",
    "Você é resposta certa no meio da minha confusão.",
    "Você tem mais brilho que tela de celular no escuro.",
    "Se eu fosse status, seria 'te esperando'.",
    "Você não é nuvem, mas vive no meu céu particular.",
    "Se você fosse temperatura, era verão com vento leve.",
    "Você é vírgula que muda todo o sentido da minha rotina.",
    "Se tua risada fosse senha, eu hackeava a vida só pra ouvir de novo.",
    "Você é melhor que café na ressaca e abraço no frio.",
    "Você tem aquela coisa que ninguém sabe explicar... mas todo mundo sente.",
    "Você é conexão estável no meio da minha instabilidade.",
    "Com você, até problema parece tutorial resolvido.",
    "Você é aquela figurinha rara que eu nunca trocaria.",
    "Você é check-in automático no meu coração.",
    "Se teu beijo fosse código, era puro JavaAmor.",
    "Você é notificação de sorte num celular antigo.",
    "Você tem o poder de parar o tempo com um só olhar.",
    "Te encontrar foi tipo descobrir atalho novo pra felicidade.",
    "Você é o backup dos meus dias bons.",
    "Teu jeito é bug no meu sistema emocional: trava tudo e eu gosto.",
    "Você é print que a vida me deixou tirar sem nem eu pedir.",
    "Se teu sorriso fosse música, eu dançava em looping.",
    "Você tem o cheiro de coisa que dá certo.",
    "Você é o tipo de pessoa que nem o tempo consegue apagar.",
    "Se tua voz fosse mensagem, era a única que eu ouvia até o fim.",
    "Você é a aba que nunca quero fechar.",
    "Seu carinho é tipo chocolate quente em dia frio: cura até pensamento ruim.",
    "Você tem mais charme que café com leite em manhã preguiçosa.",
    "Você é meu bug favorito: deixa tudo fora do controle e mesmo assim vale a pena.",
    "Se você fosse direção, eu seguia sem GPS.",
    "Com você, até o silêncio tem gosto de companhia boa.",
    "Você é aquele motivo que faz tudo valer mais a pena.",
    "Se você fosse spoiler, eu deixava estragar tudo só pra te ver logo.",
    "Você é aquela linha que falta na minha poesia.",
    "Você tem aquele 'quê' de encanto que ninguém entende, mas todo mundo sente.",
    "Você é como bom livro: quanto mais eu descubro, mais eu me apaixono."
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
    "Essa aí já fez boy gaguejar só com um 'oi' bem dado.",
    "Se eu contar o que ela fez no último rolê... o grupo silencia.",
    "Essa menina já virou assunto até de reunião de condomínio.",
    "Ela já fez um ex voltar só com um emoji.",
    "Uma vez ela passou e até o vento perdeu o rumo.",
    "Conhecida por fazer crush esquecer o nome da ex em 2 mensagens.",
    "Ela não manda indireta... ela manda saudade em alta definição.",
    "Uma vez ela piscou... e três casais discutiram no mesmo dia.",
    "Ela já deixou boy travado só com a bio do Instagram.",
    "Essa aqui fala 'bobo' de um jeito que desestrutura qualquer homem.",
    "Ela já deixou gente em crise só com o tom de voz.",
    "Se ela cruza a perna, tem gente que repensa o relacionamento.",
    "Ela é o motivo de muita terapia por aí.",
    "Já fez cara jurar amor eterno e esquecer 24h depois.",
    "Uma vez ela mandou figurinha e terminou namoro alheio.",
    "O stories dela devia ter aviso de impacto emocional.",
    "Ela tem olhar que hipnotiza e risada que vicia.",
    "Ela não precisa falar muito... a presença entrega o resto.",
    "Quando ela entra no grupo, até o ADM arruma o cabelo.",
    "Ela já virou desculpa de muita DM escondida.",
    "Se ela encosta, o sistema emocional reinicia.",
    "Já foi confundida com feitiço... porque ninguém sai igual depois.",
    "Ela responde 'nada não' e o caos começa.",
    "Se ela disser 'tô com saudade', o coração entra em colapso.",
    "Já mandou áudio que foi ouvido mais de 7 vezes.",
    "O problema não é ela... é o efeito que ela causa.",
    "Já desorganizou boy só com um elogio bem posicionado.",
    "Ela não some... ela dá espaço pra sentir falta.",
    "Tem gente que sonha com o cheiro do cabelo dela.",
    "Uma vez ela sorriu e esqueceram até a senha do celular.",
    "Conhecida por transformar silêncio em expectativa.",
    "Ela já fez clima só com a vírgula no texto.",
    "Se ela te chama de 'meu bem', prepara que a mente vai longe.",
    "Ela é o 'só mais 5 minutinhos' do coração de muitos.",
    "Quando ela cruza o olhar, ninguém desvia com facilidade.",
    "Já causou DR só por reagir com coração.",
    "Tem status que ela posta e o grupo treme.",
    "O filtro favorito dela é o que ativa suspiro alheio.",
    "Ela não causa ciúme, ela ativa radar emocional.",
    "Já tirou print e virou lembrança eterna de alguém.",
    "Ela manda áudio sussurrado e o boy perde a linha.",
    "Uma vez ela disse 'vem' e teve gente que correu 3 bairros.",
    "Ela não se atrasa... ela cria tensão.",
    "Se ela diz 'até amanhã', tem gente que nem dorme.",
    "Ela é do tipo que chega atrasada e rouba a cena.",
    "Tem gente que fica online só esperando uma mensagem dela.",
    "Ela já fez até o fone parecer beijo no ouvido.",
    "Ela manda figurinha e o clima esquenta.",
    "Ela tem frase de bio que já gerou fanfic na cabeça dos outros.",
    "Se ela digita devagar, alguém já tá suando frio.",
    "Ela já bloqueou só pra ver se iam atrás.",
    "Já criou saudade antes mesmo de sair do lugar.",
    "Ela já virou plano de fundo de pensamento alheio.",
    "Quando ela diz 'me nota', o mundo pausa.",
    "Ela responde com três pontinhos e desmonta estruturas.",
    "Tem gente que se perde só no 'oi sumido' dela.",
    "Uma vez ela olhou pro lado... e virou ponto de fuga da realidade.",
    "Ela tem o dom de transformar dúvida em desejo.",
    "Ela não precisa te tocar... ela bagunça por pensamento.",
    "Ela tem histórico de áudio que vale mais que carta de amor.",
    "Se ela manda 'boa noite', o travesseiro esquenta.",
    "Ela já causou tempestade com uma mensagem fora de hora.",
    "O modo offline dela é gatilho de ansiedade pra muita gente.",
    "Ela já trocou o clima da conversa com um 'aham'.",
    "Se ela diz 'te cuida', tem boy que pega gripe só pra ganhar mimo.",
    "Ela já deixou boy rindo pro celular no meio da rua.",
    "Uma vez ela digitou, apagou, digitou de novo... e ele ficou 2h online.",
    "Ela já fez gente entrar em grupo só pra ficar perto.",
    "O bom dia dela deveria ter trilha sonora.",
    "Ela posta indireta que parece personalizada.",
    "Ela tem print salvo no coração de alguém que não assume.",
    "Já causou saudade retroativa com um story antigo.",
    "Ela tem mais presença que Wi-Fi em dia de chuva.",
    "Se ela usar emoji errado, alguém interpreta como fim de relação.",
    "Ela não pede atenção, ela atrai sem esforço.",
    "Ela já deixou mensagem no vácuo... só pra gerar desespero.",
    "Ela já confundiu 'amizade colorida' com crush vitalício.",
    "Ela responde 'já tô deitada' e tem gente que perde o chão.",
    "Ela já fez chorar com print de mensagem antiga.",
    "Ela tem nome salvo com coração em mais de três celulares.",
    "Ela tem mais impacto que áudio de 8 segundos sem contexto.",
    "Ela já mandou 'oi?' só pra ver quem sentia falta.",
    "Ela é o tipo de lembrança que não se deleta.",
    "Ela responde 'sei não' e a dúvida vira desejo.",
    "Se ela fala 'tô com sono', o boy perde o dele.",
    "Já teve gente que guardou camisa com perfume dela por meses.",
    "Ela é a notificação favorita de muita alma distraída.",
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
