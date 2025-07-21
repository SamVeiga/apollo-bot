# Este é um trecho representativo do código, reidentado
# A versão completa deve ser ajustada diretamente no código-fonte real

def responder(msg):
    texto = msg.text.lower()
    username = f"@{msg.from_user.username}" if msg.from_user.username else ""

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
        return

    if SAUDACOES_ATIVADAS and any(saud in texto for saud in ["bom dia", "boa tarde", "boa noite", "boa madrugada"]):
        saudacao = "bom dia 😎" if "bom dia" in texto else                    "boa tarde 😎" if "boa tarde" in texto else                    "boa noite 😎" if "boa noite" in texto else                    "boa madrugada 😎"
        time.sleep(20)
        bot.reply_to(msg, saudacao, parse_mode="Markdown")
        return

    salvar_mensagem_recebida(msg)
    return