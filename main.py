import logging
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Token e dono
TOKEN = "7559286879:AAFSeGER9vX0Yav0l5L0s7fzz3OvVVOhZPg"
DONO_ID = 1481389775

# Configura log
logging.basicConfig(level=logging.INFO)

# Lista de cantadas (apenas para mulheres)
CANTADAS = [
    "Se beleza fosse crime, você já tava presa, gata. 😏",
    "Com esse charme todo, você devia ser patrimônio cultural.",
    "Me chama de teoria que eu tento te provar.",
    "Se você fosse um bug, eu deixava acontecer todo dia. 😎",
]

# Piadas genéricas
PIADAS = [
    "Por que o programador foi ao médico? Porque ele tinha um loop infinito de dor. 😂",
    "Sabe por que o Java nunca é convidado pra festas? Porque ele demora pra começar!",
    "O que um bit disse pro outro? Nos vemos no bus. 🤓",
]

# Bajulações só pro dono
BAJULACOES = [
    "Samuel chegou, agora sim o grupo tem liderança. 👑",
    "Tudo que o Samuel fala devia virar mandamento.",
    "Senhoras e senhores, o dono da moral entrou em cena.",
]

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"E aí, {update.effective_user.first_name}? O Apolo tá online e preparado pra dar close. 😎")

# Mensagem de boas-vindas
async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Salve, {member.first_name}! Seja bem-vindo(a) ao grupo. Agora segura a zoeira. 😏")

# Comando /cantada
async def cantada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username and user.username.endswith('a'):
        frase = CANTADAS.pop(0)
        CANTADAS.append(frase)
        await update.message.reply_text(f"{user.first_name}, {frase}")
    else:
        await update.message.reply_text("Cantada é só pras damas, meu parceiro. 😅")

# Comando /piada
async def piada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frase = PIADAS.pop(0)
    PIADAS.append(frase)
    await update.message.reply_text(frase)

# Resposta inteligente e personalizada
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message
    user = mensagem.from_user
    texto = mensagem.text.lower()
    citado = context.bot.username.lower() in texto or 'apolo' in texto

    if not citado:
        return

    if user.id == DONO_ID:
        frase = BAJULACOES.pop(0)
        BAJULACOES.append(frase)
        await mensagem.reply_text(f"{user.first_name}, {frase}")
    elif user.username and user.username.endswith("a"):
        frase = CANTADAS[0]
        await mensagem.reply_text(f"{user.first_name}, {frase}")
    else:
        await mensagem.reply_text(f"{user.first_name}, tu fala umas que parece piada... mas tamo junto 😂")

# Função principal
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cantada", cantada))
    app.add_handler(CommandHandler("piada", piada))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

    print("Bot Apolo rodando... 🚀")
    app.run_polling()
