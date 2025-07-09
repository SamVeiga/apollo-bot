from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    Dispatcher,
)
import os
import random

TOKEN = os.getenv("BOT_TOKEN", "7559286879:AAFSeGER9vX0Yav0l5L0s7fzz3OvVVOhZPg")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "")
DONO_ID = 1481389775

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Frases
FRASES_CANTADAS = [
    "Você tem um mapa? Me perdi no brilho dos seus olhos.",
    "Seu nome é Google? Porque tem tudo que eu procuro.",
    "Você é feita de cobre e telúrio? Porque você é Cu-Te.",
]

FRASES_PIADAS = [
    "Por que o programador foi ao médico? Porque ele tinha um bug!",
    "O que o 0 disse pro 8? Que cinto legal!",
    "Qual o peixe mais inteligente? O atum — ele é um peixe-tudo!",
]

FRASES_BAJULACAO = [
    "Samuel é tão sábio que até o Google pergunta pra ele.",
    "Samuel não erra, ele ensina.",
    "Samuel é o dono do grupo e da razão.",
]

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o Apolo 🤖")

async def cantada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(FRASES_CANTADAS))

async def piada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(FRASES_PIADAS))

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for membro in update.message.new_chat_members:
        await update.message.reply_text(f"Bem-vindo(a) {membro.first_name}!")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    nome = update.message.from_user.first_name
    id_usuario = update.message.from_user.id

    if "apolo" in texto or "@apolo_8bp_bot" in texto:
        if id_usuario == DONO_ID:
            await update.message.reply_text(random.choice(FRASES_BAJULACAO))
        elif nome.lower().endswith("a"):
            await update.message.reply_text(random.choice(FRASES_CANTADAS))
        else:
            await update.message.reply_text(random.choice(FRASES_PIADAS))

# Inicialização do bot + webhook
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("cantada", cantada))
application.add_handler(CommandHandler("piada", piada))
application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/", methods=["GET"])
async def set_webhook():
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    await bot.set_webhook(url=webhook_url)
    return "🚀 Webhook do Apolo configurado com sucesso!", 200

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")
