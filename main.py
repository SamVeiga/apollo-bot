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
    "Te encontro no intervalo entre o acaso e o inevitável.",
    "Teu silêncio é a trilha que guia minha inquietação.",
    "Quando você chega, o tempo não entende mais de pressa.",
    "Te olhar é tropeçar num mundo sem chão, mas cheio de sentido.",
    "Tu não chegou, tu invadiu com classe.",
    "Teus olhos me ensinam a esquecer o depois.",
    "Te espero sem relógio, mas com intenção.",
    "Tua ausência não some, só muda de canto.",
    "A gente nem se tocou, mas meu mundo já mudou de rumo.",
    "Você é página nova escrita com vento.",
    "Tua chegada altera meu eixo, minha rota e meu juízo.",
    "Te olho como quem vê o último pôr do sol de todos os tempos.",
    "Você não passa, você marca.",
    "Tem nome que vira vento, o teu virou furacão.",
    "Não prometo eternidade, mas teu agora me basta inteiro.",
    "Teus passos desenham caminhos que minha alma reconhece.",
    "Tu é pausa que vira trilha sonora de arrepio.",
    "Te espero no intervalo onde a coragem abraça o desejo.",
    "Não te peço nada, só que continue sendo caos com direção.",
    "Tua calma acende uma vontade que não sei nomear.",
    "Meu pensamento corre quando teu nome encosta na memória.",
    "Teu jeito de existir me desorganiza bonito.",
    "A vida me deu certezas, você bagunçou todas com charme.",
    "Entre todos os ruídos, tua ausência grita mais alto.",
    "Você não diz nada e mesmo assim faz barulho em mim.",
    "Te encontrar é como abrir janelas em dias nublados.",
    "Tu vem de mansinho e muda a arquitetura da alma.",
    "Eu queria fugir, mas tua presença me prende com liberdade.",
    "Você me atravessa sem aviso e permanece como destino.",
    "Teu sorriso vira atalho pra todas minhas vontades.",
    "Você não é caminho, é travessia.",
    "A forma como você existe bagunça minha ordem interior.",
    "Você não bate na porta, abre todas ao mesmo tempo.",
    "Se for ilusão, que me mantenha acordado.",
    "Te vejo e esqueço o que era prioridade.",
    "Você tem presença de poema que nunca se apaga.",
    "Me embriago da tua ausência como quem recita tua falta.",
    "É no teu silêncio que mora meu ruído preferido.",
    "Tua presença tem gosto de coisa que eu não sabia que precisava.",
    "Você é o erro que parece acerto disfarçado de sorte.",
    "Me perco fácil nas entrelinhas dos teus gestos.",
    "Se tua intenção era bagunçar, parabéns: fez arte.",
    "Tu é desvio que leva pro centro de mim.",
    "O mundo gira, mas tua lembrança é eixo fixo.",
    "Se o destino brinca, que brinque contigo do meu lado.",
    "Tu é pausa de um mundo que não para.",
    "Você não se explica, você se sente.",
    "Tua ausência me visita com frequência demais pra ser acaso.",
    "Tu não é porto, é mar aberto com vento bom.",
    "Te olhar é assinar contrato com o imprevisível.",
    "Seus gestos são poesia que nem rima precisa.",
    "Você entra sem bater, e mesmo assim me desmonta.",
    "Tu é caos necessário pra manter minha lucidez em risco.",
    "Tua presença é o convite que não nego nem com medo.",
    "Você não é metade, é excesso que cabe inteiro.",
    "Tu tem gosto de livro bom que não quero terminar.",
    "Você é aquele verso que a alma recita sem saber de cor.",
    "Se for pra me perder, que seja no teu olhar sem mapa.",
    "Você é intervalo entre o tédio e o encantamento.",
    "Te encontro até quando me escondo.",
    "Você vem sem prometer, e cumpre mais do que o esperado.",
    "Tu é sim dito com a entonação certa.",
    "Você é bagunça com cheiro de paz.",
    "Se teu olhar fosse canção, meu silêncio dançaria.",
    "Você não é lembrança, é insistência do agora.",
    "Tua ausência é sombra com nome.",
    "Você não é cena, é filme inteiro sem créditos finais.",
    "Tu é poesia que insiste em se repetir sem enjoar.",
    "Me perco nos teus silêncios como quem navega.",
    "Você não diz tudo, mas insinua o suficiente.",
    "Teu sorriso é geografia nova no meu mapa de vontades.",
    "Teu cheiro me lembra tudo que ainda nem vivi.",
    "Você é porto e tempestade ao mesmo tempo.",
    "Se for pra mergulhar, que seja no teu mistério.",
    "Tua calma inquieta, tua ausência pesa.",
    "Você é aquele sopro que muda tudo sem encostar.",
    "Tu é estrada que não pede pressa.",
    "Você é vírgula que muda o sentido do parágrafo.",
    "Te espero no meio da confusão, porque tu é paz.",
    "Você não é resposta, mas faz todas as perguntas calarem.",
    "Tu é vento que sopra por dentro.",
    "Você é aquele segredo que o tempo não revela.",
    "Você não precisa falar pra fazer eco.",
    "Tua sombra é mais clara do que muita presença.",
    "Te vejo no intervalo dos pensamentos desatentos.",
    "Tu é ponto final que parece reticência.",
    "Você vem com a leveza de quem carrega tempestade.",
    "Se tua presença fosse estação, eu moraria no teu clima.",
    "Você é detalhe que arrasta o enredo inteiro.",
    "Tu chega e a lógica desiste de mim.",
    "Você é intuição que insiste em acertar.",
    "Tua lembrança não some, muda de perfume.",
    "Tu não é sonho, é realidade teimosa.",
    "Você aparece até nas pausas dos meus dias corridos.",
    "Teu jeito de estar muda até o meu silêncio.",
    "Tu é descanso que acelera o coração.",
    "Você é espera que vale a pressa.",
    "Tu não me atrai, tu me leva.",
    "Você tem jeito de quem se aloja até no que não cabe.",
    "Se for pra arriscar, que seja tua presença no caos.",
    "Tua falta é cheia de presença.",
    "Você é luz baixa com intensidade alta.",
    "Te encontrar é como desobedecer o óbvio com gosto."
]

revelacoes_safadas = [
    "Essa menina aí já escreveu o nome dele no espelho embaçado depois do banho.",
    "Ela finge que ignora, mas o @ dele é o mais visitado no histórico.",
    "Diz que não liga, mas sorri quando ele aparece online.",
    "Já decorou o último horário que ele fica no grupo… só pra dar ‘boa noite’ na hora certa.",
    "Ela escuta música triste fingindo que não é por ele.",
    "Já passou 10 minutos olhando o status dele e dizendo que era só ‘curiosidade acadêmica’.",
    "Finge que dorme, mas tá esperando uma notificação dele.",
    "Já ensaiou conversa no espelho caso ele puxe assunto.",
    "Tem figurinha só pra ele… mas nunca usou.",
    "Ela fala ‘aff’, mas já sonhou com a aliança imaginária.",
    "Ela não responde rápido, mas corre quando vê que foi ele quem mandou.",
    "Já leu o perfil dele mais vezes do que o próprio currículo dela.",
    "Ela nega, mas já combinou look mentalmente caso esbarre com ele um dia.",
    "Ela diz que ele é ‘normalzinho’… mas o coração dela pensa diferente.",
    "Já fez enquete com as amigas só pra saber se devia puxar assunto.",
    "Ela jurou que ia esquecer… mas tá lembrando com mais carinho ainda.",
    "Fez playlist pra esquecer, mas toda música lembra ele.",
    "Já escreveu texto no bloco de notas e apagou pra não parecer carente.",
    "Ela diz que é só amizade, mas tá colecionando prints com coração.",
    "Ela não curte as fotos dele, mas stalkeia todas.",
    "Tem o @ dele salvo como ‘alergia’… mas vive se coçando por dentro.",
    "Já sonhou com casamento, três filhos e um gato, tudo com o rosto dele no plano.",
    "Ela fala que é só zoeira, mas sente falta quando ele não aparece.",
    "Usa indireta no status como quem não quer nada… mas torce pra ele entender tudo.",
    "Ela diz que não reparou… mas sabe até a cor da blusa que ele usou semana passada.",
    "Fala que é drama, mas tá torcendo pra ele aparecer no sonho de novo hoje.",
    "Tem notificação silenciada, mas abre o chat dele a cada meia hora.",
    "Finge que tá de boa… mas mandou o print da conversa pra três amigas com ‘olha isso!’",
    "Ela fala que não acredita em sinais… mas interpretou três só hoje por causa dele.",
    "Já fez horóscopo dos dois e ainda ficou com raiva do ascendente dele.",
    "Ela diz que é fria, mas derreteu no primeiro ‘bom dia’ que ele mandou.",
    "Já ensaiou 7 formas de esbarrar com ele no grupo sem parecer forçada.",
    "Diz que não lembra o nome dele direito, mas escreve certo com emoji e tudo.",
    "Ela jura que é só simpatia, mas deu zoom na foto de perfil mais de 3 vezes.",
    "Finge que não viu o story, mas já assistiu em 0.5x pra captar cada detalhe.",
    "Diz que não liga, mas o emoji preferido dela agora é o que ele mais usa.",
    "Já ficou brava com ele… só porque ele respondeu seco e ela já tava apegada.",
    "Ela jurou que não ia mais olhar… mas digitou o nome dele de novo agora há pouco.",
    "Diz que é coincidência, mas posta exatamente quando ele tá online.",
    "Ela diz que não sente falta… mas vive lendo conversa antiga.",
    "Já fez montagens mentais de fotos dos dois como se fosse casal de comercial.",
    "Ela chama ele de ‘doido’, mas tem carinho até no xingamento.",
    "Se faz de desligada, mas lembra até o horário em que ele deu ‘boa noite’.",
    "Já suspirou sorrindo lendo um ‘kkk’ dele.",
    "Ela diz que não cria expectativa… mas já tem trilha sonora do beijo.",
    "Finge que foi sem querer… mas escreveu o nome dele no caderno.",
    "Ela diz que foi sem querer… mas o coração acelera toda vez que ele entra no grupo.",
    "Diz que esqueceu… mas trocou a senha por algo que lembra ele.",
    "Já mandou figurinha pensando nele, só que fingiu que era aleatória.",
    "Ela diz que é só zoeira, mas ficou chateada quando ele parou de interagir.",
    "Fala que é só amigo, mas sorri diferente com ele.",
    "Já escreveu carta mental e recitou dormindo.",
    "Ela diz que não pensa nele… mas tem playlist no nome do @ dele.",
    "Ela jura que não tá apaixonada, mas reagiu com 💗 num story de comida que ele postou.",
    "Já falou o nome dele enquanto dormia — e ninguém teve coragem de rir.",
    "Ela diz que é indiferente, mas quando ele fala, até a alma presta atenção.",
    "Já digitou e apagou mensagem 4 vezes… só porque queria acertar o tom.",
    "Ela finge que não entendeu, mas entendeu e ainda criou expectativa.",
    "Diz que é só o momento… mas já criou história de 5 temporadas com ele.",
    "Tem toque de celular só pra ele, mesmo que nunca vá tocar.",
    "Ela diz que tá ocupada… mas sempre tem tempo pra responder ele.",
    "Já passou perfume pra mandar áudio.",
    "Diz que é só texto… mas leu em voz alta imaginando ele ouvindo.",
    "Fala que é só charme… mas o coração dela já alugou espaço com ele.",
    "Já ficou séria demais só porque ele tava olhando.",
    "Ela diz que não é ciumenta… mas reparou quando outra curtiu a foto dele.",
    "Ela jura que não reparou… mas decorou a bio inteira dele.",
    "Já deixou de postar story só porque ele não ia ver.",
    "Ela fala que não sente nada… mas sonhou que dançava com ele no meio da rua.",
    "Fala que não é nada… mas o nome dele virou senha de Wi-Fi.",
    "Já ensaiou um 'oi' que nunca saiu.",
    "Ela diz que não se apega… mas já sente falta do ‘bom dia’ dele.",
    "Diz que é exagero… mas chorou ouvindo uma música que ele postou.",
    "Ela fala que odeia romance… mas vive imaginando o beijo perfeito.",
    "Ela diz que não sente nada… mas se perde toda vez que ele fala com ela.",
    "Já passou o perfume preferido dele só pra postar uma selfie aleatória.",
    "Ela nega tudo… mas o olhar entrega cada linha do sentimento escondido.",
    "Ela diz que é desapegada… mas já pensou em como seria o nome dos filhos.",
    "Já planejou uma viagem só porque ele disse que queria conhecer o lugar.",
    "Ela finge que não se importa… mas o coração faz festa quando ele manda ‘oi’.",
    "Diz que não quer mais saber… mas o sorriso ainda aparece quando falam dele.",
    "Ela fala que esqueceu… mas ainda sente borboletas com o toque do nome dele.",
    "Ela fala que tá tudo bem… mas o travesseiro sabe o nome completo dele.",
    "Já respondeu com ‘kkk’ e depois apagou pra parecer desinteressada.",
    "Diz que é só amizade… mas a saudade desmente todo dia.",
    "Já postou música com legenda ambígua só pra ver se ele percebia.",
    "Ela fala que não quer… mas o coração dela já mandou convite.",
    "Diz que não presta atenção… mas sabe o número do zap dele de cabeça.",
    "Já sonhou com ele… e acordou com vontade de contar, mas não contou.",
    "Ela diz que não quer nada sério… mas levou a sério até a brincadeira.",
    "Finge que é distraída… mas sabe até o fundo da alma como ele sorri.",
    "Já mandou indireta que só ele entenderia… e torceu pra ele notar.",
    "Ela diz que não sente… mas o ‘visto por último’ dele ainda mexe com ela.",
    "Diz que não tem apego… mas tá apegada até à notificação dele.",
    "Já olhou o nome dele piscando e sorriu sozinha no escuro.",
    "Ela fala que é madura… mas borboletas não têm idade.",
    "Já deixou o celular no mudo… só pra não pirar esperando ele chamar.",
    "Ela diz que se ama em primeiro lugar… mas deixou um espacinho pra ele no meio.",
    "Já escreveu poesia mental com o nome dele e o céu do lado.",
    "Ela fala que é só coisa da cabeça… mas o coração insiste que não é.",
    "Já desejou ‘boa noite’ pro travesseiro pensando no nome dele.",
    "Ela diz que não idealiza… mas já viu filme inteiro só com a silhueta dele na mente."
    "O nome dela na conversa já vem com emoji de alerta.",
    "Tem dublagem dela em figurinha que ninguém tem coragem de abrir no trabalho."
]

respostas_submisso_dono = [
    "Ordem tua é sentença, chefe.",
    "Só apita que eu resolvo na bala (de sarcasmo).",
    "Patrão falou, o mundo que se ajeite.",
    "Aqui é tipo cão de guarda: tu manda, eu mordo.",
    "Quem te desobedecer, eu trato pessoalmente.",
    "Se é pra sujar as mãos, já tô sem luva.",
    "Não discuto, não penso — só obedeço.",
    "Se o plano é teu, o caos é comigo.",
    "A tropa sou eu, o general é tu. Simples assim.",
    "Se tu falar ‘vai’, nem pergunto ‘pra onde’.",
    "Meu papel aqui é obedecer. Pensar é luxo de chefe.",
    "O que tu manda, o mundo acata — começando por mim.",
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
        
# Verificação final: submissão ao dono
if msg.from_user.id == DONO_ID:
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

    if mencionou_bot:
        time.sleep(20)
        bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")

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
