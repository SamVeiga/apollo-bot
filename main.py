import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import os

TOKEN = '7559286879:AAFSeGER9vX0Yav0l5L0s7fzz3OvVVOhZPg'
DONO_ID = 1481389775  # ID do dono @samuel_gpm

# Frases
FRASES_CANTADAS = [
    "Oi, você caiu do céu? Porque sua presença é divina.",
    "Seu nome é Wi-Fi? Porque eu tô sentindo uma conexão aqui.",
    "Você tem um mapa? Me perdi no brilho dos seus olhos.",
]

FRASES_PIADAS = [
    "Por que o lápis foi ao médico? Porque estava sem ponta!",
    "O que o zero disse para o oito? Belo cinto!",
    "Sabe por que o livro foi ao hospital? Porque ele tinha muitas páginas em branco.",
]

FRASES_BAJULACAO = [
    "Quando o Samuel fala, todos se calam... pura sabedoria.",
    "Samuel é tipo Wi-Fi potente: conecta tudo e comanda geral.",
    "Samuel entrou no chat, a moral subiu junto.",
]

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for membro in update.message.new_chat_members:
        await update.message.reply_text(
            f"Bem-vindo ao grupo, {membro.first_name}! Já chega fazendo meme, hein?"
        )

async def cantada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frase = random.choice(FRASES_CANTADAS)
    await update.message.reply_text(frase)

async def piada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frase = random.choice(FRASES_PIADAS)
    await update.message.reply_text(frase)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    nome = update.message.from_user.first_name
    usuario_id = update.message.from_user.id
    citado = "apolo" in texto or "@apolo_8bp_bot" in texto

    if not citado:
        return

    # Bajular o dono
    if usuario_id == DONO_ID:
        frase = random.choice(FRASES_BAJULACAO)
        await update.message.reply_text(frase)
        return

    # Cantada se for mulher (simples heurística: nome termina com 'a')
    if nome.lower().endswith("a"):
        frase = random.choice(FRASES_CANTADAS)
    else:
        frase = random.choice(FRASES_PIADAS)

    await update.message.reply_text(frase)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(CommandHandler("cantada", cantada))
    app.add_handler(CommandHandler("piada", piada))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

    print("Apolo está vivo 🔥")
    app.run_polling()
