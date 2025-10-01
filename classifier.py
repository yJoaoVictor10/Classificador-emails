import re
import string
from pathlib import Path
from nltk.stem import SnowballStemmer

PALAVRAS_PARADA = {
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

radicalizador = SnowballStemmer('portuguese')
palavras_parada = PALAVRAS_PARADA

PALAVRAS_CHAVE_PRODUTIVAS = ['solicita', 'suport', 'atualiz', 'duvid']
PALAVRAS_CHAVE_IMPRODUTIVAS = ['feliz', 'obrig', 'parabén', 'agradec']

def extrair_texto_arquivo(caminho_arquivo):
    caminho = Path(caminho_arquivo)
    if caminho.suffix.lower() == '.txt':
        return caminho.read_text(encoding='utf-8', errors='ignore')
    elif caminho.suffix.lower() == '.pdf':
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return ''
        paginas_texto = []
        leitor = PdfReader(str(caminho))
        for pagina in leitor.pages:
            paginas_texto.append(pagina.extract_text() or '')
        return '\n'.join(paginas_texto)
    else:
        return ''

def preprocessar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'\S+@\S+', ' ', texto) 
    texto = re.sub(r'http\S+', ' ', texto)
    texto = re.sub(r'\d+', ' ', texto)     
    texto = texto.translate(str.maketrans('', '', string.punctuation))  

    tokens = [t for t in texto.split() if t not in palavras_parada]
    tokens_radicalizados = [radicalizador.stem(t) for t in tokens]

    return ' '.join(tokens_radicalizados)

def analisar_email(texto_preprocessado):
    pontuacao = 0
    for palavra in PALAVRAS_CHAVE_PRODUTIVAS:
        if palavra in texto_preprocessado:
            pontuacao += 2
    for palavra in PALAVRAS_CHAVE_IMPRODUTIVAS:
        if palavra in texto_preprocessado:
            pontuacao -= 2

    categoria = 'Produtivo' if pontuacao > 0 else 'Improdutivo'
    return categoria, pontuacao

def gerar_resposta_openai(texto_original, categoria, chave_openai):
    try:
        import openai
    except ImportError:
        return 'OpenAI não instalado. Instale `openai` para usar esta funcionalidade.'

    openai.api_key = chave_openai
    prompt = (
        f"Classifique o seguinte email como Produtivo ou Improdutivo e gere uma resposta adequada.\n\n"
        f"Categoria: {categoria}\nEmail:\n{texto_original}\n\nResposta sugerida:\n"
    )

    try:
        resposta = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=200,
            temperature=0.2,
        )
        return resposta.choices[0].text.strip()
    except Exception as erro:
        return f'Erro ao chamar OpenAI: {erro}'
