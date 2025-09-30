import re
import string
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from PyPDF2 import PdfReader

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stemmer = SnowballStemmer('portuguese')
stop_words = set(stopwords.words('portuguese'))

PRODUCTIVE_KEYWORDS = ['solicita', 'suport', 'atualiz', 'duvid']
UNPRODUCTIVE_KEYWORDS = ['feliz', 'obrig', 'parabén', 'agradec']


def extract_text_from_file(file_path):
    """Extrai texto de arquivos .txt ou .pdf"""
    path = Path(file_path)
    if path.suffix.lower() == '.txt':
        return path.read_text(encoding='utf-8', errors='ignore')
    elif path.suffix.lower() == '.pdf':
        text_pages = []
        reader = PdfReader(str(path))
        for page in reader.pages:
            text_pages.append(page.extract_text() or '')
        return '\n'.join(text_pages)
    else:
        return ''


def preprocess_text(text):
    """Normaliza, remove emails, urls, números, pontuação, stopwords e aplica stemming"""
    text = text.lower()
    text = re.sub(r'\S+@\S+', ' ', text) 
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'\d+', ' ', text)     
    text = text.translate(str.maketrans('', '', string.punctuation))  

    tokens = [t for t in text.split() if t not in stop_words]
    stemmed_tokens = [stemmer.stem(t) for t in tokens]

    return ' '.join(stemmed_tokens)


def analyze_email(preprocessed_text):
    """Classifica o email em Produtivo ou Improdutivo usando palavras-chave"""
    score = 0
    for kw in PRODUCTIVE_KEYWORDS:
        if kw in preprocessed_text:
            score += 2
    for kw in UNPRODUCTIVE_KEYWORDS:
        if kw in preprocessed_text:
            score -= 2

    category = 'Produtivo' if score > 0 else 'Improdutivo'
    return category, score


def generate_response_with_openai(original_text, category, openai_api_key):
    """
    Gera uma resposta automática via OpenAI (opcional).
    Requer pacote `openai` instalado e chave de API válida.
    """
    try:
        import openai
    except ImportError:
        return 'OpenAI não instalado. Instale `openai` para usar esta funcionalidade.'

    openai.api_key = openai_api_key
    prompt = (
        f"Classifique o seguinte email como Produtivo ou Improdutivo e gere uma resposta adequada.\n\n"
        f"Categoria: {category}\nEmail:\n{original_text}\n\nResposta sugerida:\n"
    )

    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=200,
            temperature=0.2,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f'Erro ao chamar OpenAI: {e}'