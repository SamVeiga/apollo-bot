
import json
import os
import random
from datetime import datetime, timedelta

def load_phrases(file_path):
    """Lê um arquivo JSON e retorna a lista de frases"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_phrases(file_path, data):
    """Salva uma lista de dados em um arquivo JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def can_send_response(user_id, user_history, max_per_day=3):
    """Verifica se o usuário pode receber resposta automática hoje (limite 3 vezes)"""
    today = datetime.now().date()
    responses_today = [d for d in user_history.get(user_id, []) if d.date() == today]
    return len(responses_today) < max_per_day

def can_send_now(user_id, user_history):
    """Verifica se passou pelo menos 1 hora desde a última resposta do usuário"""
    if user_id not in user_history:
        return True
    last_response = max(user_history[user_id])
    return datetime.now() - last_response >= timedelta(hours=1)

def pick_phrase(phrases, used_phrases, days_limit=5):
    """Escolhe uma frase aleatória sem repetir as usadas nos últimos X dias"""
    cutoff_date = datetime.now() - timedelta(days=days_limit)
    recent_used = {phrase for phrase, date in used_phrases.items() if date > cutoff_date}
    available = [p for p in phrases if p not in recent_used]
    if not available:
        available = phrases
    return random.choice(available)

def get_user_gender(user_id, homens_dict, mulheres_dict):
    """Retorna o gênero do usuário ('homem', 'mulher' ou None)"""
    if str(user_id) in homens_dict:
        return 'homem'
    elif str(user_id) in mulheres_dict:
        return 'mulher'
    else:
        return None
