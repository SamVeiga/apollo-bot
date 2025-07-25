from flask import Flask, request
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

# === CONFIGURACOES === #
ID_DONO = 1481389775
ID_GRUPO = -1002363575666
LIMITE_DIARIO = 3
INTERVALO_HORAS = 1
NOME_BOT = "Apolo"
USERNAME_BOT = "@Apolo"

# === CAMINHOS === #
BASE = os.path.dirname(__file__)
PASTAS = {
    'frases': os.path.join(BASE, 'frases'),
    'membros': os.path.join(BASE, 'membros'),
    'data': os.path.join(BASE, 'data')
}

ARQUIVOS = {
    'homens': os.path.join(PASTAS['membros'], 'homens.json'),
    'mulheres': os.path.join(PASTAS['membros'], 'mulheres.json'),
    'historico': os.path.join(PASTAS['data'], 'historico_apollo.json'),
    'dicionario': os.path.join(PASTAS['data'], 'dicionario_apollo.json')
}

# === FUNCOES UTILITARIAS === #
def carregar_json(path, default):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hora_atual():
    return datetime.now()

def saudacao_do_dia():
    hora = hora_atual().hour
    if 5 <= hora < 12:
        return 'bom_dia'
    elif 12 <= hora < 18:
        return 'boa_tarde'
    else:
        return 'boa_noite'

def usuario_genero(username):
    homens = carregar_json(ARQUIVOS['homens'], [])
    mulheres = carregar_json(ARQUIVOS['mulheres'], [])
    if username in mulheres:
        return 'mulher'
    elif username in homens:
        return 'homem'
    return 'desconhecido'

def selecionar_frase(tipo, genero, username):
    historico = carregar_json(ARQUIVOS['historico'], {})
    chave = f"{username}_{tipo}"
    frases = carregar_json(os.path.join(PASTAS['frases'], f"{tipo}_{'para_' + genero}s.json"), [])
    usadas = historico.get(chave, [])

    disponiveis = [f for f in frases if f not in usadas]
    if not disponiveis:
        historico[chave] = []
        disponiveis = frases
    escolhida = disponiveis[0] if disponiveis else None

    if escolhida:
        usadas.append(escolhida)
        historico[chave] = usadas[-15:]  # controla as últimas 15 frases usadas
        salvar_json(ARQUIVOS['historico'], historico)
    return escolhida

def pode_responder(username):
    historico = carregar_json(ARQUIVOS['historico'], {})
    hoje = hora_atual().date().isoformat()
    chave = f"{username}_respostas"
    dados = historico.get(chave, [])

    agora = hora_atual()
    if len(dados) >= LIMITE_DIARIO:
        if all(datetime.fromisoformat(dt).date() == agora.date() for dt in dados):
            return False
    if dados and (agora - datetime.fromisoformat(dados[-1])).seconds < INTERVALO_HORAS * 3600:
        return False

    dados.append(agora.isoformat())
    historico[chave] = [dt for dt in dados if datetime.fromisoformat(dt).date() == agora.date()]
    salvar_json(ARQUIVOS['historico'], historico)
    return True

# === ENDPOINT PRINCIPAL === #
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    msg = data.get('message') or {}
    texto = msg.get('text', '').strip()
    username = msg.get('from', {}).get('username', '').lower()
    chat_id = msg.get('chat', {}).get('id')

    if not texto or chat_id != ID_GRUPO:
        return 'ignorado'

    genero = usuario_genero(username)

    # Comandos de administracao
    if texto.startswith('/adicionar_homem') and (msg['from']['id'] == ID_DONO):
        alvo = texto.split()[-1].replace('@', '').lower()
        homens = carregar_json(ARQUIVOS['homens'], [])
        if alvo not in homens:
            homens.append(alvo)
            salvar_json(ARQUIVOS['homens'], homens)
        return 'homem adicionado'

    if texto.startswith('/adicionar_mulher') and (msg['from']['id'] == ID_DONO):
        alvo = texto.split()[-1].replace('@', '').lower()
        mulheres = carregar_json(ARQUIVOS['mulheres'], [])
        if alvo not in mulheres:
            mulheres.append(alvo)
            salvar_json(ARQUIVOS['mulheres'], mulheres)
        return 'mulher adicionada'

    # Dicionario
    if texto.endswith('?') and texto.lower().startswith('o que '):
        dicionario = carregar_json(ARQUIVOS['dicionario'], {})
        chave = texto.lower().strip('?')
        resposta = dicionario.get(chave)
        if resposta:
            return resposta
        return "Não sei, mas posso aprender."

    # Saudacoes
    if any(s in texto.lower() for s in ['bom dia', 'boa tarde', 'boa noite']):
        tipo = saudacao_do_dia()
        frases = carregar_json(os.path.join(PASTAS['frases'], f"{tipo}.json"), [])
        return frases[0] if frases else ''

    # Menção direta ao Apolo
    if NOME_BOT.lower() in texto.lower() or USERNAME_BOT.lower() in texto.lower():
        tipo = 'mencao_de_homem' if genero == 'homem' else 'mencao_de_mulher'
        frases = carregar_json(os.path.join(PASTAS['frases'], f"{tipo}.json"), [])
        return frases[0] if frases else ''

    # Frase automática
    if pode_responder(username):
        tipo = 'insultos' if genero == 'homem' else 'xavecos'
        frase = selecionar_frase(tipo, genero, username)
        return frase or ''

    return 'ok'

if __name__ == '__main__':
    app.run(port=5000, debug=True)
