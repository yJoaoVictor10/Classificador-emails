import re
import string
from pathlib import Path
from nltk.stem import SnowballStemmer

# Stopwords portuguesas já incluídas
STOP_WORDS_PORTUGUESE = {
    'a','à','ao','aos','aquela','aquelas','aquele','aqueles','aquilo','as','até',
    'com','como','da','das','de','dela','delas','dele','deles','depois','do','dos',
    'e','ela','elas','ele','eles','em','entre','era','eram','éramos','essa','essas',
    'esse','esses','esta','está','estamos','estão','estas','estava','estavam','este',
    'estes','eu','foi','foram','há','isso','isto','já','lhe','lhes','mais','mas','me',
    'mesmo','meu','meus','minha','minhas','na','nas','não','nem','no','nos','nós',
    'nossa','nossas','nosso','nossos','num','numa','o','os','ou','para','pela','pelas',
    'pelo','pelos','por','qual','quando','que','quem','se','seu','seus','sua','suas',
    'também','te','tem','têm','teu','teus','teu','teve','tinha','tinham','toda','todas',
    'todo','todos','tu','tua','tuas','um','uma','você','vocês','vos'
}

stemmer = SnowballStemmer('portuguese')
stop_words = STOP_WORDS_PORTUGUESE

PRODUCTIVE_KEYWORDS = ['solicita', 'suport', 'atualiz', 'duvid']
UNPRODUCTIVE_KEYWORDS = ['feliz', 'obrig', 'parabén', 'agradec']

def extract_text_from_file(file_path):
    """Extrai texto de arquivos .txt ou .pdf"""
    path = Path(file_path)
    if path.suffix.lower() == '.txt':
        return path.read_text(encoding='utf-8', errors='ignore')
    elif path.suffix.lower() == '.pdf':
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return ''
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
    """Gera resposta automática via OpenAI, se chave disponível"""
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
