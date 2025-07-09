import random
import os
from telegram import Update, ChatType
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Configs do bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
DONO_USERNAME = os.getenv("DONO_USERNAME", "samuel_gpm").lower()

# Frases para o Apolo

CANTADAS = [
    "E aí, gata, caiu do céu ou caiu na zoeira do grupo? 😏",
    "Se beleza fosse argumento, você já tinha fechado o debate.",
    "Tá me devendo uma conversa, mulher inteligente dessas não aparece todo dia.",
    "Com você por aqui, só falta a zoeira melhorar ainda mais!",
]

PIADAS = [
    "Por que o livro foi ao médico? Porque ele tinha muitas páginas!",
    "O que o tomate disse para a batata? Nada, tomate não fala.",
    "Você sabe o que o zero disse pro oito? Belo cinto!",
    "Sabe por que o Apollo não briga? Porque ele ganha no deboche 😎",
]

FRASES_BAJULACAO = [
    "Se o Apolo fala, o Samuel reina. Ordem natural das coisas.",
    "Grupo bom é grupo com Samuel presente. O resto só acompanha.",
    "Diante de Samuel, até os deuses se calam. Respeita o chefe.",
]

BEM_VINDO = [
    "Salve, @{}! Chegou quem faltava pro rolê ficar completo.",
    "Chegou a lenda @{}! Se acomoda e bora zoar.",
    "Avisa que @{} chegou e trouxe o caos! Bem-vindo(a).",
]

# Utilitários

def eh_mulher(username: str) -> bool:
    # Simples suposição: username termina com 'a' para ser mulher
    return username is not None and username.lower().endswith('a')

# Handlers

async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        nome = member.username or member.first_name or "ninguém"
        msg = random.choice(BEM_VINDO).format(nome)
        await update.message.reply_text(msg)

async def cmd_cantada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CANTADAS), reply_to_message_id=update.message.message_id)

async def cmd_piada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(PIADAS), reply_to_message_id=update.message.message_id)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    texto = msg.text.lower()
    chat_type = msg.chat.type

    # Só responde em grupos
    if chat_type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return

    # Só responde se for citado (nome ou username do bot)
    bot_user = (await context.bot.get_me()).username.lower()
    if bot_user not in texto and "apolo" not in texto:
        return

    usuario = msg.from_user
    nome = usuario.first_name or usuario.username or "alguém"
    username = (usuario.username or "").lower()

    # Bajula o dono
    if username == DONO_USERNAME:
        resposta = random.choice(FRASES_BAJULACAO)
        await msg.reply_text(resposta, reply_to_message_id=msg.message_id)
        return

    # Flerta só com mulher (zoeira, nada meloso)
    if eh_mulher(username):
        resposta = random.choice(CANTADAS)
        await msg.reply_text(f"{nome}, {resposta}", reply_to_message_id=msg.message_id)
        return

    # Se não é dona e não mulher, responde com deboche/ironia
    resposta = f"{nome}, nem você salva essa, vou passar a vez. 😎"
    await msg.reply_text(resposta, reply_to_message_id=msg.message_id)

# Setup e execução do bot

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("cantada", cmd_cantada))
    app.add_handler(CommandHandler("piada", cmd_piada))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("🤖 Apollo iniciado! Pronto pra zoar o grupo 24h.")
    app.run_polling()
