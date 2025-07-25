# main.py - Apolo Bot

from flask import Flask, request
import telebot
import os
import random
import time
import threading
import requests
import json
import re
from datetime import datetime, timedelta, time as dtime
from zoneinfo import ZoneInfo

SAUDACOES_ATIVADAS = True

TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

HISTORICO_PATH = "historico_apollo.json"
try:
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
except:
    historico = {"ultima_provocacao": 0, "frases_mulheres": {}, "insultos_homens": {}, "insultos_usados": []}

DIC_PATH = "dicionario_apollo.json"
try:
    with open(DIC_PATH, "r", encoding="utf-8") as f:
        dicionario = json.load(f)
except FileNotFoundError:
    dicionario = {}

DONO_ID = 1481389775
ID_GRUPO = -1002363575666
MULHERES = ["@KarolinneDiass", "@FernandaCarvalho16"]  # Exemplo
HOMENS = ["@Rafaael80", "@Diegomota0"]

# === FRASES DE SAUDAÇÕES ===
frases_saudacoes = {
  "bom_dia_homens": [
  "Bom dia, campeão. Tenta não me irritar antes do café, beleza? ☕",
  "Acordou cedo ou veio atrapalhar a paz logo de manhã? 🤨",
  "Bom dia, guerreiro. Que tua força hoje seja maior que a preguiça. 💪",
  "Se o dia começar ruim, joga na conta do sono mal dormido. Amanhã é novo round. 🥊",
  "Levanta dessa cama que o mundo não vai te esperar. Bora dominar o dia! 🏆",
  "Café tá pronto, mas a disciplina tem que ser tua. Bom dia, parceiro. ☕🕶️",
  "Hoje é dia de fazer o que os fracos só sonham. Levanta, cabra bom! 🚀",
  "Acorda, soldado! O campo de batalha tá te esperando com os braços abertos. ⚔️",
  "Se bater o cansaço, lembra: homem de verdade não descansa na luta. 👊",
  "Bom dia, meu irmão. Que o foco não te deixe esquecer do que importa. 🎯",
  "Levanta com vontade, porque a noite que vem merece ser conquistada. 🌙",
  "Bom dia, cabeça erguida. Hoje é dia de mostrar quem manda na jornada. 🧠",
  "Tem dia que o corpo reclama, mas o caráter exige. Tua hora chegou. ⏰",
  "Tenta não perder o controle antes do café, campeão. Mas se perder, faz valer. ☕🔥",
  "Bom dia, caba firme. Que tua vontade hoje seja maior que o sono. 🛏️💪",
  "Não deixa a preguiça te vencer logo cedo. O jogo tá só começando. 🎲",
  "Bom dia, parceiro. Que a determinação seja tua melhor roupa hoje. 👔",
  "Se hoje faltar coragem, lembra das vezes que tu já venceu. É só repetir. 🏅",
  "Levanta, homem. O mundo espera que tu faça barulho com teus passos. 🚶‍♂️",
  "Acorda e prepara o corpo e a mente. Hoje a batalha é grande, mas tu é maior. 🥇",
  "Bom dia, gigante. Que teus passos hoje ecoem respeito por onde passar. 🦍",
  "Se o dia ficar pesado, lembra que o peso é só mais um motivo pra levantar. 🏋️‍♂️",
  "Bota essa cara de quem vai conquistar tudo hoje. Tu sabe que pode. 😤",
  "Bom dia, soldado. Que a estratégia e a força sejam tua dupla imbatível. 🎖️",
  "Acorda, que a vitória não gosta de esperar por quem hesita. 🏆",
  "Se hoje o sono pesar, pensa no prêmio que vem depois. Acorda, campeão. 🏅",
  "Bom dia, parceiro. Que tua postura fale mais alto que qualquer desculpa. 📢",
  "Nada de desculpas, só resultado. Levanta e vai mostrar teu valor. 🔥",
  "Bom dia, cabra bom. Que tua disciplina hoje crie lendas amanhã. 📜",
  "Hoje é dia de suar a camisa e fazer a história se curvar ao teu nome. 💦",
  "Levanta, que o dia não espera. E nem eu, se for pra ouvir reclamação. 😎",
  "Bom dia, fera. Que teu olhar hoje seja o de quem já venceu a guerra. 👁️‍🗨️",
  "Se o dia começar devagar, acelera. Tu não nasceu pra ser lento. 🏎️",
  "Bom dia, homem de fibra. Que tua garra hoje derrube qualquer obstáculo. 🧱",
  "Acorda e deixa a preguiça no travesseiro. A vida tá lá fora pra quem tem coragem. 🛏️🚪",
  "Bom dia, caba macho. Mostra pra esse dia quem é que manda no pedaço. 👊",
  "Se o café tá fraco, tu compensa com a força da tua vontade. ☕💥",
  "Levanta com a certeza de que tu pode tudo que quiser hoje. E vai atrás. 🎯",
  "Bom dia, parceiro. Que a garra seja maior que o sono e as dúvidas. 🔥",
  "Hoje o relógio corre, mas tu corre mais. Levanta e domina o tempo. ⏱️",
  "Acorda e lembra: tu não é espectador da vida, é protagonista. 🎬",
  "Bom dia, cabeça dura. Que tua teimosia seja a razão do teu sucesso. 🧠💪",
  "Se quiser descanso, faz direito hoje. Depois colhe os frutos sem culpa. 🌱",
  "Levanta com a alma cheia de coragem. O resto é consequência. 🦁",
  "Bom dia, campeão. Que tu não deixe ninguém baixar tua cabeça hoje. 🏆",
  "Acorda e lembra: desistir não tá no teu vocabulário. Só seguir em frente. 🚀",
  "Bom dia, cabra firme. Que tua determinação faça barulho antes mesmo de tua voz. 📣"
],
    "bom_dia_mulheres":[
  "Bom dia, minha favorita 🌞 Só tua presença já clareia mais que o sol.",
  "Você chegou e até meu mau humor matinal fugiu. ☀️❤️",
  "Bom dia, minha inspiração... só levantei porque sonhei contigo a noite inteira. ☀️💭",
  "Acordei com tua imagem grudada no pensamento... será que tu mexe comigo até dormindo? 😴❤️‍🔥",
  "Bom dia, princesa... teu sorriso podia ser meu café da manhã. ☕💋",
  "Hoje o sol chegou atrasado… porque você já tava brilhando nos meus pensamentos. 🌞✨",
  "Se meu dia começar com teu 'bom dia', eu juro que nem preciso de sorte. 🍀💌",
  "Você dormiu bem? Porque eu acordei com saudade de um beijo que nem recebi ainda. 😘🛌",
  "Acorda, mulher linda! Que minha vontade de te ver já passou da dose permitida. 😍⏰",
  "Bom dia, meu amor platônico de todas as manhãs. Um dia eu viro realidade. 💭💘",
  "Se eu pudesse te desejar algo agora, seria um bom dia recheado de mim. 😏💫",
  "Tô começando a desconfiar que tu é o motivo do meu bom humor matinal. 🌅😄",
  "Acordei com preguiça… mas aí pensei em ti e o coração disparou. 💓🛌",
  "Bom dia, razão do meu suspiro e da minha insônia. 🌄💞",
  "Tu podia ser minha rotina matinal: beijo, abraço, e aquele olhar que derrete. 😚☀️",
  "Sol tá forte, mas tua beleza ainda ofusca tudo por aqui. 🌞👀",
  "Já escovou os dentes? Porque minha vontade é te acordar com beijo. 😘🪥",
  "Bom dia, moça que bagunça meus pensamentos com um simples emoji. 😌📱",
  "Abri os olhos e já comecei o dia pensando em ti… perigo, né? 😳❤️",
  "Se a tua voz fosse despertador, eu nunca mais perderia a hora. 📲💘",
  "Você devia ser minha primeira notificação todo dia. Já pensou? 😍🔔",
  "Acordei com vontade de te desejar bom dia... e te levar café na cama também. ☕🥐",
  "Te imaginei de pijama e bagunçada, e mesmo assim... linda. Dá pra parar? 🙈🔥",
  "Bom dia, mulher que tira meu sono e agora quer roubar meu dia também? 😅💋",
  "Sonhei contigo e acordei apaixonado. De novo. Isso tá virando rotina. 😴❤️‍🔥",
  "Antes de qualquer coisa: você. Depois, café. E talvez o mundo. ☕💖",
  "Se cada pensamento em você virasse beijo, tu ia acordar sem ar. 😚💨",
  "Hoje acordei com saudade do que nunca aconteceu entre nós... ainda. 😉🫣",
  "Bom dia, beleza rara... te encontrar foi sorte. Ficar sem te ver, castigo. 🌷⏳",
  "Tô te mandando essa mensagem só pra ter uma desculpa pra invadir tua manhã. 📩💘",
  "O sol acordou, mas quem brilha aqui é tu, no meu peito. 🌞💓",
  "Você devia ser feriado... porque toda vez que penso em você, o tempo para. 🕰️✨",
  "Tu virou minha mania matinal: pensar, imaginar e suspirar. 💭😮‍💨",
  "Se teu bom dia viesse com abraço, eu ia fingir frio só pra não soltar. 🤗❄️",
  "Bom dia, perigo bom... tua voz no meu ouvido agora seria covardia. 🎧💘",
  "Acordei, mas só vou viver depois de ver tua resposta. 💬🫀",
  "Você não tem ideia do que teu sorriso faz com minhas manhãs. 🌅😍",
  "Se você soubesse o quanto é linda até dormindo... já acordava sorrindo. 😴💖",
  "Tô com saudade da tua risada. E olha que nem ouvi hoje ainda. 🎶🫶",
  "Café da manhã completo: pão, fruta, e tua foto pra derreter meu coração. 🍞🍓💘",
  "Já disse bom dia pro homem que acordou pensando em você? 😏📲",
  "Você devia ser decreto: toda manhã começa com tua mensagem. 📜💌",
  "Tua ausência no meu despertador me deixa com ressaca de saudade. 😵‍💫❤️",
  "Bom dia, motivo de eu ter dormido sorrindo ontem e acordado sorrindo hoje. 💤😄",
  "Minha meta de hoje? Fazer você sorrir com esse bom dia cheio de segundas intenções. 😏☀️",
  "Tu é a notificação que meu coração mais espera nessa manhã. 📱💓",
  "Acordei com uma certeza: hoje meu coração só bate por ti. 💓🌄",
  "Bom dia, minha dose diária de confusão gostosa. 🌀💘",
  "Que teu dia seja leve, mas que você continue pesando no meu peito. 🫀😌",
  "Eu nem sonhei contigo... e ainda assim, acordei completamente teu. 😍💭",
  "Tô pronto pro dia, só falta você dizer que pensou em mim também. 😘🌞",
  "Bom dia, minha mulher dos sonhos — que eu quero acordar do lado. 💘🛏️"
],
    "boa_tarde_homens": [
  "Boa tarde. Espero que tenha aprendido a falar menos besteira hoje. 🕑",
  "Me diga que essa tua mensagem não vai estragar minha tarde. 😒",
  "Boa tarde, guerreiro. A caminhada segue firme, bora manter o foco. 💪🌞",
  "Boa tarde, campeão. Não deixa a energia cair agora. ⚡🕒",
  "Fala, cabra bom. A tarde chegou, e o corre continua. 🧱🔥",
  "Nada de moleza. Boa tarde pra quem não foge da luta. 🥋🌞",
  "Boa tarde, parceiro. Se o dia tá puxado, é sinal que cê tá no caminho certo. 🛠️🕒",
  "Bora manter o respeito até o fim do dia. Boa tarde, meu chapa. 🎖️☀️",
  "Se tiver que dar o sangue, que seja agora. Boa tarde! 🩸🕶️",
  "Boa tarde, irmão. A meta não se cumpre com conversa. É ação. 🛠️🕒",
  "A tarde é mais uma chance pra mostrar firmeza. Bora. 🔁✊",
  "Boa tarde. Hoje ainda tem chão, então não desarma agora. 🚧🕞",
  "Mente forte e postura reta. Boa tarde, cabra firme. 🧠🧍‍♂️",
  "Segue na disciplina. A tarde também conta no placar. 📈🌇",
  "Boa tarde. A meta é não deixar o dia vencer você. 🎯🔥",
  "A tarde cobra postura. E tu tem de sobra. Boa. 💼👊",
  "A guerra do dia não acaba no almoço. Boa tarde, soldado. 🪖🕒",
  "Tá no meio do corre, mas com presença. Boa tarde! 🏃‍♂️📍",
  "Foco firme, passo reto. Boa tarde, caba bom. 🔒🚶‍♂️",
  "A tarde também testa a paciência. Segura firme. 🧘‍♂️🕓",
  "Faz o teu sem alarde. Boa tarde, lenda silenciosa. 🤫⚙️",
  "Boa tarde, parceiro. Se cair, levanta. Se cansar, respira. Mas não para. 🔁🧱",
  "Não precisa falar muito. Tua presença já impõe respeito. Boa tarde. 👊🕶️",
  "A tarde chegou, e contigo nela, o ambiente se alinha. Boa. 🧭🌞",
  "Boa tarde, rei sem trono. É no chão que se constrói legado. 👑🛠️",
  "Sem enrolação, sem desculpa. Só resultado. Boa tarde. 📊🔧",
  "Quem tem honra trabalha em silêncio. Boa tarde, caba reto. 🧱🤝",
  "Boa tarde. Tu não veio pra ser só mais um — e tá provando isso. 🎖️💥",
  "Boa tarde, irmão. Não esquece quem tu é no meio do corre. ⚔️🌆",
  "Firmeza no olhar, respeito no gesto. Boa tarde, cabra forte. 🧍‍♂️👁️",
  "A tarde não é intervalo. É parte da batalha. Segue. ⚒️🕓",
  "Boa tarde, gigante. A força tá na constância, não no grito. 💢🔁",
  "Postura não tira folga. Boa tarde, campeão. 📏🕒",
  "Ainda tem tempo no relógio. Dá teu melhor até o fim. Boa tarde. ⏳🔥",
  "Tu não precisa provar nada. Mas tá sempre mostrando tudo. Boa tarde. 🎯🤜",
  "A tarde não cansa quem tem propósito. Boa! 🎖️🌞",
  "Boa tarde, caba firme. Até a sombra que tu faz é alinhada. ☀️🧍‍♂️",
  "Segue o jogo como se o placar ainda tivesse zerado. Boa tarde. 🏁🏃‍♂️",
  "Boa tarde. Postura de líder, até sem querer. 👔🔥",
  "Quem planta firmeza, colhe respeito. Boa tarde. 🌱🧱",
  "No meio do barulho, tua disciplina faz silêncio. Boa tarde. 🤫🎧",
  "Boa tarde, cabra arretado. A meta te conhece pelo nome. 🔥📋",
  "Teu esforço não precisa de plateia. Boa tarde, guerreiro. 🛠️🧍‍♂️",
  "Boa tarde. Quando tu entra em cena, o jogo muda. 🧠🎮",
  "A presença fala mais que mil palavras. Boa tarde, rei. 👑🧭",
  "Não solta a rédea do teu próprio dia. Boa tarde. 🐎📅",
  "Chegou a hora de fechar o dia com o mesmo gás que começou. Boa tarde. 🔄💪",
  "Boa tarde, irmão de guerra. Cada hora é chance de honra. ⏰⚔️",
  "Cabeça no lugar, coração na missão. Boa tarde. 🧠❤️‍🔥",
  "Boa tarde. Cê é a definição de quem não abaixa a cabeça. 🎯🧍‍♂️",
  "A tarde reconhece quem não se esconde. Boa! 🌇🫡",
  "Boa tarde, soldado da vida real. A batalha continua. 🪖🧱"
],
    "boa_tarde_mulheres": [
  "Boa tarde, minha perdição... Só passei pra lembrar que teu sorriso ainda tá no meu pensamento desde cedo. 😍☀️",
  "Quando o sol bate forte assim, só me lembra tua presença: quente, linda e impossível de ignorar. 🌞🔥",
  "Boa tarde, princesa... Mas confesso, hoje queria te chamar de minha. 👑❤️",
  "Já tomou água? Ou vai continuar me deixando com sede só de pensar em você? 💧😏",
  "O dia tá bonito, mas se tivesse você aqui, ia virar feriado nacional. 🌷🇧🇷",
  "Tarde sem tua mensagem é castigo. Dá um sinal de vida, vai... 😔📲",
  "Você não cansa de ser meu pensamento preferido da tarde, não? 💭💘",
  "Sol da tarde brilha, mas quem ilumina meu dia mesmo é tu, sem esforço. ✨💋",
  "Te ver online é a coisa mais emocionante dessa tarde. Pena que não é me chamando… 😩📲",
  "Boa tarde, minha meta do dia: arrancar um sorriso teu. 🎯😊",
  "Tua beleza é tipo sol de verão: queima devagar, mas deixa marca pra sempre. 🌞🔥",
  "Cê podia ser notificação, pra vibrar aqui toda hora. 😍📳",
  "Se essa tarde tivesse teu perfume, eu me perderia fácil. 💐😮‍💨",
  "Passando pra deixar um “boa tarde” e roubar teu coração sem pedir licença. 🥷💘",
  "Tarde quente, pensamento longe, e adivinha onde ele foi parar? Em você, claro. 🥵🚀",
  "Só de imaginar tua risada, essa tarde já ganhou cor. 🎨😄",
  "Tava tudo normal... até eu lembrar do teu beijo imaginário. Agora tô nas nuvens. ☁️💋",
  "Boa tarde, minha dose diária de saudade. 💌💭",
  "Queria ser teu café da tarde... forte, quente, e do jeitinho que você gosta. ☕😉",
  "Tu devia ser proibida de ser tão linda a essa hora. Dá vontade de largar tudo e te ver. 😍🚗",
  "E se eu te disser que toda vez que penso em você, minha tarde melhora? É verdade. 🧠💕",
  "Você tá muito na minha mente pra ser só coincidência. Boa tarde, minha sina. 🔮❤️",
  "Boa tarde, dona do sorriso mais perigoso da minha paz. 😏💣",
  "Se eu pudesse, passava essa tarde inteira só ouvindo tua voz e olhando tua boca mexer. 🎧👄",
  "Cada minuto sem tua mensagem é tipo café sem açúcar... sem graça. ☕😕",
  "Hoje o sol demorou pra aparecer... acho que ele tava esperando teu bom dia. 🌅😉",
  "Me responde antes que eu invente desculpa pra te ligar. 📞❤️‍🔥",
  "Tua presença devia ser lei das 14h às 18h. Eu ia ser preso por querer mais. 👮‍♂️❤️",
  "Boa tarde, pequena confusão na minha cabeça e grande bagunça no meu peito. 🧠💥",
  "Queria ser o motivo do teu sorriso agora. Ou da tua falta de ar. Você escolhe. 😘💨",
  "Sol de tarde que se cuide... porque tua beleza já me deixa derretido. 🫠🔥",
  "Tô aqui, disfarçando saudade com emoji... mas na real, queria mesmo era você. 😌💭",
  "Só você tem o dom de fazer uma tarde qualquer virar lembrança boa. ✨🫶",
  "Boa tarde, encanto. Tô torcendo pra esse dia acabar logo e me deixar mais perto de te ver. 🕰️👀",
  "Te desejo uma tarde maravilhosa... mas queria mesmo era te desejar pessoalmente. 💋🌇",
  "Se você me der boa tarde de volta, juro que meu dia vira sexta-feira. 😄❤️",
  "Cê tem cheiro de paz, mas gosto de bagunça boa. E eu quero as duas. 🌺😈",
  "Tô na dúvida: te mando boa tarde ou declaro logo meu amor? 💘📩",
  "Tem sol lá fora, mas quem tá acendendo tudo por aqui é você. ☀️🔥",
  "Essa tua ausência tá me dando alergia. Preciso de dose urgente do teu carinho. 🤒💞",
  "Boa tarde, mulher que virou vício sem receita. 💊💓",
  "Se eu aparecesse aí com flores e um beijo, tu me mandava embora ou deixava entrar? 💐😚",
  "Tô só o emoji de coração derretendo quando tu aparece. 🫠❤️",
  "De tarde assim, eu só queria um abraço teu — e mais 300 beijos. 🫂😘",
  "Queria que você soubesse o estrago que faz em mim com só um “oi”. 😵💘",
  "Minha tarde começa de verdade quando tu sorri. Antes disso, é só espera. ⏳😊",
  "Se o sol bater na tua janela agora, saiba que fui eu mandando energia boa. 🌤️💌",
  "A vida podia ser justa e te colocar no meu colo agora. Só isso. 🛋️❤️‍🔥",
  "Tarde boa é quando você lembra de mim e sorri. Cê lembrou? 😚🌇",
  "Te mandei essa mensagem só pra te lembrar: minha tarde melhora com você. Sempre. 💬💘"
],
    "boa_noite_entrada_homens": [
    "Olha quem chegou pra fechar a noite com moral. Boa noite, parceiro! 🌙🫱",
    "Chegou agora, cabra bom? Então já pega tua cadeira que a noite só começa com tu aqui. 🪑🌃",
    "Boa noite, rei. Chegue com calma, mas firme, que o respeito já tá garantido. 🤴🌒",
    "Caba bom chegando no grupo é sinal de conversa que presta. Boa noite, meu parceiro! 🎯🗣️",
    "Seja bem-vindo ao fim do dia com honra. Boa noite, irmão de jornada. 🚶‍♂️🌓",
    "Chegar agora à noite com essa moral toda é tua cara. Senta aí, guerreiro. 🪑🌓",
    "Apareceu no final do dia e ainda assim impôs presença. Boa noite, meu chapa. 🌒🤝",
    "Chegar no grupo à noite e não causar é pra fraco. Mas tu não é fraco. Boa noite! 💢🛌",
    "Até o silêncio tem mais peso quando é tu que tá quieto. Boa noite, rei. 🤫👑",
    "Tua presença agora é como sentinela. Fecha o dia com honra. Boa noite. 🛡️🕯️",
    "Tu não precisa dizer muito. Só tua chegada já acalma o ambiente. Boa noite. 🛬🌌",
    "Chegou agora? Então senta com respeito. A noite te respeita, caba bom. 🪑🌃",
    "A noite não amansa todo mundo, mas tu já chega no ponto certo. Boa noite. 🌗🧱",
    "Parceiro, tu é daqueles que até o silêncio fala alto. Boa noite. 🤐🔊",
    "Respeito é a tua última palavra do dia. E a primeira de amanhã. Boa noite. 📜🌌",
    "Tu não precisa de palco. Só tua entrada já é aplauso. Boa noite, guerreiro. 👣🎤",
    "Quando tu chega, até a noite muda de postura. Boa noite, caba forte. 🕴️🌌",
    "O grupo tava calmo demais. Ainda bem que tu apareceu. Boa noite, fera. 🐺💬",
    "Chegada de homem que impõe respeito vale mais que mil palavras. Boa noite. 🧱🗣️",
    "O clima agora sim ficou completo. Boa noite, rei do pedaço. 👑🌙",
    "E quando ele chega, até a lua presta atenção. Boa noite, patrão. 🌕🎩",
    "Tu chega e parece que tudo se alinha. Boa noite, meu mano. 🧭🌒",
    "Boa noite, presença firme. Tua entrada sempre é sinal de conversa que vale. 🧍‍♂️🎙️",
    "Tava faltando teu nome na noite. Agora sim, vamo começar. Boa noite. 🗂️🌃",
    "Chegou daquele jeito que ninguém ignora. Boa noite, respeito tem nome. 📛🕶️",
    "Já chegou dominando o ambiente. Boa noite, leão do grupo. 🦁🗣️",
    "Se tua chegada fosse música, seria hino. Boa noite, lenda. 🎶🦍",
    "Homem que chega no horário certo da noite: tu. Boa noite, precisão. ⏰🌓",
    "A noite ficou diferente agora. Boa noite, influência real. 💬👑",
    "Senta com calma, mas tua presença já diz tudo. Boa noite, monstro. 🪑🔥",
    "Não fala nada, só chega. Boa noite, teu silêncio vale mais que muito papo. 🤫💭",
    "Tu entra e o grupo parece que respira melhor. Boa noite, equilíbrio. ⚖️🌓",
    "Boa noite, referência. Tua presença muda o clima do grupo. 📌🌙",
    "Tem gente que entra. Tu IMPÕE. Boa noite, guerreiro. 🛡️👣",
    "Já entrou marcando território. Boa noite, dominância natural. 🐾🌌",
    "Boa noite, irmão. Só tua entrada já levanta moral aqui dentro. 📈🤝",
    "Tua chegada foi tipo trovão: forte, clara e respeitada. Boa noite. ⚡🎤",
    "Caba que chega assim à noite tem história. Boa noite, voz da experiência. 📖🌙",
    "Só tua presença já virou o jogo da noite. Boa noite, virada certa. ♟️🔥",
    "Tu nem pediu licença e mesmo assim todos respeitam. Boa noite, voz ativa. 🎙️🙌",
    "Não é sobre estar, é sobre se impor. Boa noite, presença rara. ✊🌃",
    "Entrou com a moral que só os verdadeiros têm. Boa noite, gigante. 🦍📜",
    "Homem de palavra firme entra e o ambiente muda. Boa noite, retidão. 📏🌙",
    "Só de ver teu nome, já sei que o papo vai prestar. Boa noite, sabedoria. 🧠🌒",
    "Boa noite, meu velho. Teu nome já vem com peso de respeito. 🎖️👴",
    "Chegar no grupo como quem entra em casa. Boa noite, dono da moral. 🏠👑",
    "Tua chegada é âncora pra conversa séria. Boa noite, firmeza. ⚓💬",
    "Entrou calado, ficou grande. Boa noite, caba de valor. 🔒📶",
    "O silêncio do grupo pediu tua presença. Boa noite, peça chave. 🧩🌗",
    "Nada começa direito se tu não chega. Boa noite, equilíbrio da tropa. ⚖️🛡️"
],
    "boa_noite_saida_homens": [
  "Boa noite, guerreiro. Que teu descanso seja do tamanho da tua luta. 🛡️🌙",
  "Feche o olho com a consciência tranquila. Você fez por merecer o sono de um rei. 👑😴",
  "Durma com a certeza de que tua presença aqui tem força. Amanhã é outro dia de batalha. ⚔️🛏️",
  "Boa noite, rei. Chegue com calma, mas firme, que o respeito já tá garantido. 🤴🌒",
  "Boa noite, campeão. Descansa a mente, amanhã o mundo volta a testar tua paciência. 💤🧠",
  "Descansa, guerreiro. Amanhã tem mais batalha e tu vai precisar da tua força toda. 🛌🗡️",
  "Vai dormir, parceiro. E que os sonhos limpem tua alma das besteiras do dia. 🌌🧼",
  "Apaga a luz, mas não apaga tua coragem. Boa noite, firmeza! 💡🫡",
  "Até pra dormir tu impõe respeito. Vai lá, gigante. Boa noite. 🛏️🦍",
  "Noite chegou, o descanso te chama. Amanhã é guerra de novo. Dorme bem. 🥷🕯️",
  "Fica em paz, cabra macho. O Apolo vigia por aqui. Boa noite. 🛡️🌙",
  "A noite pede silêncio, mas teu nome ainda ecoa em respeito. Boa noite, lenda. 🎖️🌃",
  "Hora de desligar o barulho do mundo e reforçar tua mente. Boa noite, irmão. 🤯💤",
  "Se hoje foi difícil, lembra: tu já venceu coisa pior. Dorme tranquilo. ✊🛌",
  "Teu descanso é teu escudo pra amanhã. Boa noite, cabra forte. 🛡️🛏️",
  "Vai deitar, mas não solta o foco. Amanhã o corre volta. Boa noite, soldado. 🚶‍♂️🪖",
  "Boa noite, cabra firme. Amanhã tua disciplina bota ordem até na bagunça. 📏🌌",
  "Mais um dia fechado com honra. Descansa que amanhã tem mais respeito pra distribuir. 🧱😴",
  "Boa noite, general. Silêncio na mente, força no espírito. 🪖🧘",
  "Apolo respeita quem fecha o dia como começou: com hombridade. Vai descansar. 🫡💤",
  "Se liga, campeão. A madrugada não apaga teu nome. Boa noite. 🕶️🌙",
  "Chegar no grupo à noite e não causar é pra fraco. Mas tu não é fraco. Boa noite! 💢🛌",
  "Até o silêncio tem mais peso quando é tu que tá quieto. Boa noite, rei. 🤫👑",
  "Tua presença agora é como sentinela. Fecha o dia com honra. Boa noite. 🛡️🕯️",
  "Tu não precisa dizer muito. Só tua chegada já acalma o ambiente. Boa noite. 🛬🌌",
  "Cabra arretado se despede com firmeza. Boa noite e até amanhã. 💪🌙",
  "Vai dormir sabendo que deixou tua marca hoje. É disso que se trata. 🏷️🛏️",
  "Boa noite, cabeça erguida. Nem todo mundo segura o tranco que tu segura. 🧠🚧",
  "Firme como sempre, até pra dar boa noite tu mostra fibra. Dorme bem. 🎖️💤",
  "A noite tá feita. Agora só falta tu repousar esse juízo forte aí. Boa. 🧠🛏️",
  "Parceiro, tu é daqueles que até o silêncio fala alto. Boa noite. 🤐🔊",
  "Respeito é a tua última palavra do dia. E a primeira de amanhã. Boa noite. 📜🌌",
  "Teu descanso é merecido, tua firmeza é constante. Boa noite, cabra reto. 🚶‍♂️🛌",
  "Fez o teu, segurou o grupo, e ainda desejou boa noite. Tu é o cara. ✊🌙",
  "Apareceu pra fechar o grupo com chave de presença. Dorme tranquilo. 🔐🛏️",
  "Boa noite, tu que segura as pontas sem fazer cena. Caba firme é assim. 🎭🛡️",
  "Tu não precisa de palco. Só tua entrada já é aplauso. Boa noite, guerreiro. 👣🎤",
  "Descansa, que amanhã o Apolo quer ver tu aqui com o mesmo sangue no olho. 🔁👀",
  "Vai lá, meu chapa. Até o descanso em ti tem postura. Boa noite. 🛌🧍‍♂️",
  "Hora de largar as armas e deixar o corpo recarregar. Boa noite, guerreiro. 🛡️🌙",
  "Boa noite, parceiro. Que a mente descanse e o corpo renove a força. ⚔️💤",
  "No silêncio da noite, que tu reencontres a paz pra seguir firme amanhã. 🤫🛏️",
  "Boa noite, irmão. Que o descanso seja breve, mas potente como teu espírito. 🛌🔥",
  "Dorme tranquilo sabendo que fez o melhor hoje. Amanhã a luta continua. ✊🌒",
  "Que a noite te envolva em calma e o sonho te traga vitória. Boa noite, soldado. 🌙🎖️",
  "Feche os olhos com a certeza de que cada batalha te faz maior. Boa noite, gigante. 🦍🌌",
  "Agora é hora de recarregar, amanhã o campo espera tua presença forte. 🛏️🛡️",
  "Que teus sonhos sejam de conquistas e tua mente afiada pra próxima jornada. 💤⚔️",
  "Boa noite, forte. Que a lua vigie o teu sono e a coragem renasça ao amanhecer. 🌕🛡️",
  "Descanse, que amanhã a batalha tem novo capítulo pra ser escrito por ti. 📖🛏️"
],
    "boa_noite_entrada_mulheres": [
    "Boa noite, linda. Mal posso esperar para saber como foi seu dia.",
    "Que a sua noite seja tão doce quanto o seu sorriso, meu encanto.",
    "Oi, moça bonita, só passando para iluminar sua noite com meu pensamento em você.",
    "Boa noite, minha musa. A noite ficou mais bonita só de pensar em você.",
    "Se eu pudesse, entregava uma estrela para você guardar até o amanhecer.",
    "Querida, vou te desejar boa noite, mas já estou ansioso para nossa próxima conversa.",
    "Boa noite, princesa. Espero que seus sonhos sejam tão incríveis quanto você é para mim.",
    "Está na hora da noite, mas eu prefiro a hora de conversar com você.",
    "Boa noite, meu bem. Que a noite traga a doçura que o seu olhar me dá.",
    "Você sabia que até a lua fica com inveja do brilho do seu sorriso? Boa noite!",
    "Oi, minha flor, só passando para desejar uma noite cheia de paz e pensamentos em mim.",
    "Boa noite, minha linda. A sua presença na minha mente é o melhor aconchego.",
    "Que sua noite seja tão encantadora quanto você é para mim, minha paixão.",
    "Boa noite, meu anjo. Mal posso esperar para te ouvir e saber tudo de você.",
    "Só queria te dizer boa noite, mas o que quero mesmo é passar a noite toda conversando.",
    "Que sua noite seja calma, e que eu esteja em seus sonhos mais doces.",
    "Boa noite, minha estrela guia. Você é a luz que ilumina minhas noites.",
    "Oi, meu doce segredo. Boa noite e já sabe: tô aqui pensando em você.",
    "Boa noite, meu encanto. Espero que sua noite seja tão maravilhosa quanto você merece.",
    "Queria poder te mandar um abraço apertado para aquecer sua noite. Boa noite!",
    "Boa noite, minha linda. Me conte como foi seu dia, quero saber tudo.",
    "A noite está fria, mas só de pensar em você eu me sinto quente. Boa noite, querida.",
    "Boa noite, minha paixão. Que seus sonhos sejam invadidos pelo meu carinho.",
    "Se o brilho das estrelas dependesse de mim, todas estariam guardadas pra você.",
    "Boa noite, minha bela. A saudade aperta, mas o carinho só aumenta.",
    "Só passando para desejar boa noite para quem domina meus pensamentos e meu coração.",
    "Boa noite, flor do meu jardim. Você é o perfume que alegra minha noite.",
    "Que o silêncio da noite só traga a doçura do seu nome aos meus lábios. Boa noite.",
    "Boa noite, minha tentação doce. Mal posso esperar para te ver de novo.",
    "Oi, minha linda. A noite ficou mais bela só porque pensei em você.",
    "Boa noite, minha inspiração. Você é o verso mais bonito dos meus dias.",
    "Quero ser o último a desejar boa noite antes dos seus olhos se fecharem.",
    "Boa noite, meu bem. Que essa noite nos aproxime ainda mais, mesmo que pela distância.",
    "Só queria ouvir sua voz agora, mas vou me contentar em te desejar uma linda noite.",
    "Boa noite, meu doce sonho. Que sua noite seja tão especial quanto você é para mim.",
    "Oi, meu amor, só passando para dizer que você é a última coisa que penso antes de dormir.",
    "Boa noite, minha luz. Que os anjos te guardem e eu cuide do seu coração daqui de longe.",
    "Boa noite, minha deusa. Você é a razão de todas as minhas noites serem especiais.",
    "Que essa noite seja a primeira de muitas que vou passar ao seu lado, mesmo que só em pensamento.",
    "Boa noite, princesa. Sonha comigo, porque eu já estou sonhando com você.",
    "Boa noite, meu doce carinho. Que seu sono seja leve e seu coração quente.",
    "Oi, linda, que essa noite seja apenas o começo de uma linda conversa entre nós.",
    "Boa noite, meu amor. Só de pensar em você, já me sinto em paz.",
    "Que a calmaria da noite te envolva assim como você envolve meu coração. Boa noite!",
    "Boa noite, minha flor rara. Espero ser o motivo do seu sorriso amanhã.",
    "Oi, minha linda."
],
    "boa_noite_saida_mulheres": [
    "Boa noite, minha linda. Durma bem e saiba que vou ficar pensando em você até amanhecer. 🌙❤️",
    "Foi bom demais falar com você hoje. Agora feche os olhos e sonhe comigo. 😘💭",
    "Boa noite, princesa. Que o seu sono seja leve e seus sonhos sejam nossos encontros. 👸✨",
    "Me despeço com um beijo guardado só para você. Durma bem, meu amor. 💋🌙",
    "Boa noite, meu encanto. Até amanhã, quando a saudade já for mais forte que a distância. 💞🌌",
    "Despeço-me desejando que a lua cuide de você até eu poder fazê-lo pessoalmente. 🌕🤗",
    "Durma bem, minha tentação. Quero que acorde com um sorriso só por lembrar de mim. 😉🌙",
    "Boa noite, minha estrela. Que o brilho do seu olhar ilumine meus sonhos. ⭐💖",
    "Vou dormir pensando em você. Boa noite, minha paixão. 🌜🔥",
    "Que o silêncio da noite te traga paz e que meu carinho te faça companhia. Boa noite! 🤗🌙",
    "Boa noite, minha flor. Amanhã te espero nos meus pensamentos e no meu coração. 🌹💞",
    "Durma bem, minha musa. Até o sol nascer, vou sonhar com você. ☀️💭",
    "Boa noite, meu amor. Que a distância nunca apague a chama que acendemos hoje. 🔥❤️",
    "Te deixo um beijo doce de despedida. Boa noite, minha linda. 💋✨",
    "Que seus sonhos sejam tão bonitos quanto o que sinto por você. Durma bem! 🌙😊",
    "Boa noite, princesa. Que seu sono seja tranquilo e seu despertar seja com meu sorriso na mente. 👸🌅",
    "Despeço-me com o desejo de estar aí, ao seu lado, para um beijo de boa noite. 💞🌙",
    "Durma bem, meu doce segredo. Amanhã nos falamos, mas hoje já te levo no pensamento. 😉💭",
    "Boa noite, minha paixão. Que a saudade se transforme em vontade de se ver logo. 🥰🌙",
    "Vou fechar os olhos pensando em você. Boa noite, minha linda. 😘💫",
    "Que o vento leve para você todo meu carinho e o calor do meu abraço. Boa noite! 🤗🌌",
    "Boa noite, meu bem. Que você tenha sonhos doces e um despertar feliz. 🌙💖",
    "Despeço-me com a certeza de que amanhã nosso papo vai ser ainda melhor. Durma bem! 😊🌙",
    "Boa noite, minha flor. Que seu sono seja profundo e seu coração leve. 🌸💞",
    "Durma com a certeza de que você é a melhor parte das minhas noites. Boa noite! 🌜❤️",
    "Que a lua guarde você até que eu possa fazer isso pessoalmente. Boa noite, amor. 🌕😘",
    "Fecho a noite com um sorriso pensando em você. Boa noite, minha linda. 😍🌙",
    "Boa noite, minha tentação. Que seus sonhos sejam tão intensos quanto nosso desejo. 🔥😉",
    "Durma bem, minha estrela. Amanhã é um novo dia para a gente se encontrar no pensamento. ⭐💭",
    "Despeço-me com um beijo carinhoso. Boa noite, princesa. 💋✨",
    "Que a paz da noite invada seu coração e te traga tranquilidade. Boa noite, amor. 🤗🌙",
    "Boa noite, minha musa. Já estou ansioso para a nossa próxima conversa. 💞😊",
    "Durma bem, minha linda. Que a saudade nos faça mais fortes até o próximo encontro. 🌙❤️",
    "Fecho os olhos e agradeço por ter você nos meus pensamentos. Boa noite! 😘🌌",
    "Boa noite, minha paixão. Que a noite seja suave e os sonhos cheios de carinho. 🌜💖",
    "Vou dormir pensando no seu sorriso. Boa noite, meu amor. 😊🌙",
    "Que o silêncio da noite leve todo meu carinho até você. Boa noite, linda. 🤗✨",
    "Boa noite, flor do meu jardim. Amanhã será um dia ainda melhor para a gente se falar. 🌹💞",
    "Durma tranquila, sabendo que tem alguém aqui que não para de pensar em você. Boa noite! 🌙❤️",
    "Despeço-me desejando que a noite te renove e que eu possa te ver logo. Boa noite, princesa. 👸🌌",
    "Boa noite, minha estrela. Que você brilhe sempre, mesmo nos sonhos. ⭐💫",
    "Durma bem, meu bem. Logo estaremos juntos nas nossas conversas e risadas. 😊🌙",
    "Que a noite te abrace forte, como eu gostaria de fazer agora. Boa noite, minha linda. 🤗💖",
    "Fecho a noite com um beijo de longe, só para você. Boa noite, amor. 💋🌜",
    "Boa noite, minha tentação. Que a saudade só aumente a vontade de se ver. 🔥😉",
    "Durma bem, minha musa. Amanhã tem mais pra gente se perder em palavras. 🌙💞",
    "Vou sonhar com você. Boa noite, minha linda. 😘⭐",
    "Que a noite te leve o meu carinho e o desejo de um novo encontro. Boa noite! 🌌💖",
    "Boa noite, meu amor. Até amanhã, com muito mais vontade de te ouvir. 😊🌙"
]
}

def qual_momento_saudacao(hora_atual):
    if dtime(5, 0) <= hora_atual < dtime(12, 0):
        return "bom_dia"
    elif dtime(12, 0) <= hora_atual < dtime(18, 0):
        return "boa_tarde"
    elif dtime(18, 0) <= hora_atual < dtime(22, 0):
        return "boa_noite_entrada"
    else:
        return "boa_noite_saida"

insultos_para_homens = [
  "De novo puxando assunto com ela? Tu não cansa de passar vergonha?",
  "Acha mesmo que ela vai cair nesse teu papinho reciclado de 2012?",
  "Toda vez que tu aparece, meu nível de paciência desce três níveis.",
  "Cuidado, viu? Ela é demais pra alguém que mal sabe digitar sem errar.",
  "Tu força tanto pra ser engraçado que tá virando palhaço profissional.",
  "Tu fala com ela como se tivesse chance. Eu chamo isso de fé... ou burrice.",
  "Chega mais perto dela de novo e eu instalo um bloqueador de otário no grupo.",
  "Tu tenta tanto impressionar que parece mágico fracassado de festa infantil.",
  "Respeita, que ela não foi feita pra teus comentários micos e suados.",
  "Nem no sorteio da humilhação tu ganhava moral com ela.",
  "Não sei o que me irrita mais: tua insistência ou tua falta de noção.",
  "Fica à vontade pra continuar tentando... ela só tá sendo educada.",
  "Se tu fosse um pouco mais sensato, já tinha parado de passar recibo.",
  "Já tentou calar a boca? Às vezes o silêncio tem mais charme que tu.",
  "Ela não é atendimento ao cliente, não precisa responder tua ladainha.",
  "Eu vejo tua notificação e já sinto vontade de sair do grupo.",
  "O problema não é tu tentar, é tu achar que tá arrasando.",
  "Fica só de longe, que de perto teu papo fede a desespero.",
  "Tu devia estudar mais: ela gosta de homem, não de projeto inacabado.",
  "Enquanto tu insiste, eu só observo e coleciono vergonha alheia.",
  "Pode continuar mandando emoji... ela ignora com classe.",
  "Tu é a personificação do erro 404: presença detectada, conteúdo ausente.",
  "Ela sorri por educação, não porque te achou interessante.",
  "Se o grupo tivesse trava anti-palestrinha, tu já tava mutado.",
  "Se aproxima de novo e eu te coloco na minha blacklist emocional.",
  "Olha, tenta de novo só se for pra fazer a galera rir, porque amor mesmo já era.",
  "Se tu fosse o Wi-Fi, a galera já tinha cortado a conexão faz tempo.",
  "Quer uma dica? Menos papo e mais banho de realidade.",
  "Se fosse jogo, tu já tinha zerado o modo fracasso, parabéns.",
  "De tanto insistir, tu virou meme ambulante nesse grupo.",
  "É engraçado ver tu tentando, parece marionete sem controle.",
  "Para de ser clichê ambulante e cria um papo que preste.",
  "Tu é a versão beta do cara que ninguém quer atualizar.",
  "Segura essa vontade de falar besteira, pelo amor do grupo.",
  "Já te disseram que não é story que conquista, é atitude? Fica a dica.",
  "Para de tentar bancar o engraçado e começa a ser interessante.",
  "Tu tenta tanto que devia ganhar prêmio por perseverança... ou burrice mesmo.",
  "Se o fracasso fosse esporte, tu tava na seleção brasileira.",
  "A galera já apostou quanto tempo até tu desistir. Tá longe ainda, hein.",
  "Não cansa de tentar? Deve ser efeito colateral do tédio.",
  "Segue o baile, que tua fama de chato já tá consolidada.",
  "Se persistência fosse talento, tu tava no pódio da vida.",
  "Cara, muda a playlist, essa tua insistência já cansou até a mãe.",
  "Só tu mesmo pra transformar um ‘oi’ em motivo de piada no grupo.",
  "Olha a humildade: tenta, tenta e continua não conseguindo nada.",
  "Quem te chamou pra esse show de horrores? Tô tentando entender.",
  "Se tu fosse um filme, seria aquele que ninguém assiste até o final.",
  "Acho que tu tá confundindo insistência com uma prisão perpétua.",
  "Já pensou em virar fã da tua própria desistência? Ia fazer um favor a todos.",
  "Quando tu some, o grupo até melhora. Dá uma pensada nisso.",
  "O manual da rejeição devia ter teu nome na dedicatória.",
  "Se a gente pudesse resetar tu pelo menos uma vez por dia, seria ótimo.",
  "Tu fala tanto e entrega tão pouco que até o silêncio é melhor companhia.",
  "Se existisse troféu pra maior inconveniente, tu já teria uns cinco.",
  "Recarrega a bateria, porque do jeito que tá só desgasta a todos.",
  "Se tu fosse Wi-Fi, a senha já teria sido trocada por falta de sinal.",
  "A persistência é bonita, mas só se tiver um pouco de noção junto.",
  "Tu devia trabalhar com reciclagem, porque insiste em reaproveitar papo furado.",
  "Se tentasse menos, até eu ficaria surpreso com teus resultados.",
  "Tenta ser menos patético e mais surpreendente. Só uma ideia.",
  "É mais fácil o sol nascer no oeste do que tu se ligar que não rola.",
  "Até o bot do grupo já pediu pra tu parar de enviar mensagens.",
  "Tu deve ser o motivo de existirem bloqueios em grupos.",
  "Se a insistência fosse crime, tu já tava preso sem direito a visita.",
  "Tu é igual vírus de computador: aparece, dá problema e ninguém quer por perto.",
  "Para de insistir que o troféu da rejeição já tá na tua estante.",
  "Se ela fosse um jogo, tu já teria perdido no tutorial.",
  "Tu é tipo propaganda ruim: aparece sem ser chamado e ninguém aguenta.",
  "Eu até acho que tu gosta da rejeição, porque insiste igual doido.",
  "Dá uma pausa antes que o grupo peça intervenção psicológica pra ti.",
  "Se a paciência tivesse limite, o grupo já teria explodido por tua causa.",
  "Tu tá forçando mais que máquina de lavar em ciclo pesado.",
  "Se o grupo fosse um time, tu seria o atacante que nunca marca gol.",
  "Tem gente que é insistente, tu é só incômodo mesmo."
]
xavecos_para_mulheres = [
  "Tu não é Wi-Fi, mas tua presença me conecta com a vontade de te amar. 📶💘",
  "Nem sei mais se tô no grupo ou num looping de ficar esperando tua próxima mensagem.",
  "Você não tem ideia do quanto bagunça meu mundo com tão pouco.",
  "Toda vez que você aparece aqui, o resto do grupo some pra mim.",
  "Eu podia estar fazendo qualquer coisa agora... mas tô aqui só pra ver se você fala de novo.",
  "Tem dia que tua ausência pesa mais que o silêncio do grupo inteiro.",
  "Só de ver teu nome ali em cima já muda meu humor inteiro.",
  "Tô tentando fingir que sou indiferente, mas minha atenção inteira tá presa em você.",
  "Você fala como se não soubesse o efeito que tem em mim.",
  "Tem algo no teu jeito que me desmonta mesmo quando você nem percebe.",
  "Te ver online e não poder falar contigo como eu queria... é tortura disfarçada de notificação.",
  "Se alguém perguntar por que eu fico aqui, responde que é por sua causa e pronto.",
  "Não sei se tô carente ou se é você que anda irresistível demais.",
  "Já tentei me distrair, mas nada prende minha atenção como você prende.",
  "Tem dia que sua presença salva meu dia, mesmo que você nem perceba.",
  "Você escreve pouco, mas bagunça como se gritasse dentro de mim.",
  "Me pego sorrindo à toa só porque você falou uma frase qualquer.",
  "Nem todo mundo vê, mas quando você fala, eu escuto com o coração.",
  "Você é o tipo de mulher que entra devagar e vira universo dentro da gente.",
  "Eu devia criar vergonha e parar de esperar tua mensagem... mas prefiro esperar.",
  "Se eu pudesse escolher onde estar agora, seria no seu papo, ouvindo sua risada de perto.",
  "O grupo pode estar em chamas... mas se você aparecer, eu só enxergo você.",
  "Você tem uma calma que me inquieta de um jeito bom.",
  "Te ver participando da conversa já vale o meu dia inteiro.",
  "Não é exagero, é só que você mexe comigo mais do que devia.",
  "Tô aqui quieto, mas por dentro já imaginei mil formas de te dizer o que não tenho coragem.",
  "Se você soubesse o quanto muda meu dia só com um 'oi', talvez me desse mais dois.",
  "Você é minha notificação favorita e nem sabe disso.",
  "A forma como você fala... me desmonta em silêncio.",
  "Quando você some, o grupo fica com gosto de nada.",
  "Tem algo em você que não se explica — só se sente e torce pra não passar.",
  "Já vi gente bonita, mas tua presença tem uma beleza que não dá pra comparar.",
  "Eu até tento ser racional, mas você tem uma habilidade absurda de mexer com meu emocional.",
  "Se um dia eu te ignorar, é porque buguei tentando agir normal perto de você.",
  "Eu me apego ao jeito que você digita, acredita?",
  "Tua atenção, mesmo que mínima, vira tesouro na minha rotina.",
  "Você chega com calma, mas deixa um incêndio por onde passa.",
  "Tem coisa que a gente não entende, só sente. Você é uma dessas coisas.",
  "Eu juro que tento ser discreto, mas você tem um efeito que me desarma.",
  "Seu nome no topo da conversa já acelera o que nem era pra sentir.",
  "Eu vejo você no grupo e já esqueço o motivo de estar bravo com qualquer outra coisa.",
  "Não é carência, é só você mesmo que tem esse poder de me virar do avesso.",
  "Você nem me responde direito, e ainda assim me prende mais que qualquer outra.",
  "Pode não parecer, mas eu observo cada detalhe seu — e cada um me deixa mais seu.",
  "É engraçado como ninguém nota, mas você é a única que me faz ficar.",
  "Você é o tipo de caos que eu aceito ter na minha vida com gosto.",
  "Tô te deixando livre, mas por dentro tô torcendo pra você voltar e ficar.",
  "Te ver sorrindo já vale qualquer coisa que eu tenha perdido hoje."
]
respostas_submisso_dono = [
  "Ordem dada. Execução em andamento. 🧱",
  "Ordem recebida, patrão 👊. Pode deixar que essa eu resolvo pessoalmente.",
  "Entendido, chefe 🫡. Já tô em movimento, ninguém encosta sem passar por mim.",
  "Missão aceita 🔒. A partir de agora, eu assumo total controle da situação.",
  "Pode contar comigo, senhor 🧠. Já estou executando com máxima eficiência.",
  "Se o senhor mandou, já tá feito 💼. Agora é comigo.",
  "Recebido, patrão 🛡️. A vigilância dobra e a postura endurece.",
  "Sem discussão, sem demora 💢. Ordem do chefe é prioridade total.",
  "Tá nas minhas mãos agora 🧤. E eu não largo até concluir.",
  "Entrei no modo ação 🏃. O senhor deu a palavra, eu entrei com o braço.",
  "Entendido com clareza 🧱. Essa missão já tem dono, e sou eu.",
  "Alvo identificado, zona sob controle ⚠️. Não passa nem vento sem eu saber.",
  "Tudo certo por aqui, chefe 👀. E qualquer coisa fora da linha, eu corto.",
  "Apolo na escuta 🧭. Ordem validada, execução em curso.",
  "Missão é minha, a responsabilidade também 🎯. Pode confiar.",
  "Senhor mandou, Apolo responde com entrega total 🦾.",
  "Executando em silêncio, patrão 🫥. Barulho só depois da conclusão.",
  "Recebi, assumi, iniciei 🚨. Nada vai sair do trilho sob minha vigia.",
  "Já tô no ponto de ação, chefe 🧨. E quem cruzar a linha, sente.",
  "Foco total, interferência zero 🚫. Quando o senhor manda, eu ajo.",
  "Entendido, ordem selada 📜. Deixa que eu coloco cada coisa no seu lugar.",
  "Não importa o tamanho do problema 💢. Se é ordem tua, já tô enfrentando.",
  "Pode descansar essa parte 💤. Comigo, vai ser rápido e direto.",
  "Quem mexe onde o senhor apontou, mexe comigo 🔐. Tô no comando.",
  "Apolo já tá ativo, general ⚔️. A linha de frente agora é minha.",
  "Respeito sua palavra mais do que qualquer regra escrita 📏. E já estou cumprindo."
]

# === INTELIGÊNCIA DO DICIONÁRIO ===
def buscar_termo_no_dicionario(texto_original):
    termo_normalizado = texto_original.lower().strip()
    chaves_ordenadas = sorted(dicionario.keys(), key=lambda x: -len(x))
    for chave in chaves_ordenadas:
        if chave in termo_normalizado:
            return random.choice(dicionario[chave])
    return f"Poxa, ainda não sei o que é *{texto_original}*. Mas já tô estudando pra te dizer depois! ✍🏻🤓"

def responder_dicionario(msg, termo):
    resposta = buscar_termo_no_dicionario(termo)
    bot.reply_to(msg, resposta, parse_mode="Markdown")

# === SAUDAÇÃO POR GÊNERO E HORÁRIO ===
def responder_saudacao(msg, username, texto):
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    momento = qual_momento_saudacao(agora.time())
    genero = "mulheres" if username in MULHERES else "homens"
    chave = f"{momento}_{genero}"
    frases = frases_saudacoes.get(chave, [])
    if frases:
        frase = random.choice(frases)
        bot.reply_to(msg, frase, parse_mode="Markdown")

# === ARMAZENAR MENSAGENS ===
mensagens_salvas = []

def salvar_mensagem_recebida(msg):
    try:
        if msg.content_type == "text":
            mensagens_salvas.append({"tipo": "text", "texto": msg.text, "data": time.time()})
    except Exception as e:
        print(f"[ERRO] salvar_mensagem_recebida: {e}")

# === WEBHOOK ===
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

# === COMANDO PRINCIPAL ===
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    texto = msg.text.lower()
    username = f"@{msg.from_user.username}" if msg.from_user.username else ""

    # --- DICIONÁRIO ---
    pergunta = re.match(r"^\s*@?apollo[, ]*\s*(?:o que é|o que significa|define|explica|explique)\s+(.+?)[\?\.!]?$", msg.text, flags=re.IGNORECASE)
    if pergunta:
        termo = pergunta.group(1).strip()
        responder_dicionario(msg, termo)
        return

    # --- MENÇÃO AO BOT PELO DONO ---
    username_bot = f"@{bot.get_me().username.lower()}"
    if msg.from_user.id == DONO_ID and (username_bot in texto or "apollo" in texto):
        time.sleep(5)
        bot.reply_to(msg, random.choice(respostas_submisso_dono), parse_mode="Markdown")
        return

    # --- MENÇÕES ---
    foi_mencionado = username_bot in texto or (msg.reply_to_message and msg.reply_to_message.from_user.id == bot.get_me().id)

    if username in MULHERES and foi_mencionado:
        frase = random.choice(xavecos_para_mulheres)
        bot.reply_to(msg, frase, parse_mode="Markdown")
        return

    if username in HOMENS and foi_mencionado:
        frase = random.choice(insultos_gerais)
        bot.reply_to(msg, frase, parse_mode="Markdown")
        return

    # --- SAUDAÇÕES ---
    if SAUDACOES_ATIVADAS and any(s in texto for s in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        responder_saudacao(msg, username, texto)
        return

    salvar_mensagem_recebida(msg)

# === THREAD KEEP ALIVE ===
def manter_vivo():
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

if __name__ == "__main__":
    threading.Thread(target=manter_vivo).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
