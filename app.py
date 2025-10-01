from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from classifier import analisar_email, preprocessar_texto, gerar_resposta_openai, extrair_texto_arquivo

PASTA_UPLOAD = '/tmp/uploads'
EXTENSOES_PERMITIDAS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PASTA_UPLOAD
app.secret_key = os.environ.get('CHAVE_SECRETA_FLASK', 'troque_para_uma_chave_secreta_real')

if not os.path.exists(PASTA_UPLOAD):
    os.makedirs(PASTA_UPLOAD)

def arquivo_permitido(nome_arquivo):
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar():
    texto_email = request.form.get('email_text', '').strip()

    # Verifica se houve upload de arquivo
    if 'email_file' in request.files and request.files['email_file'].filename != '':
        arquivo = request.files['email_file']
        if arquivo and arquivo_permitido(arquivo.filename):
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            arquivo.save(caminho_arquivo)
            texto_email = extrair_texto_arquivo(caminho_arquivo)
        else:
            flash('Formato de arquivo não permitido. Use apenas .txt ou .pdf')
            return redirect(url_for('inicio'))

    if not texto_email:
        flash('Por favor, insira um texto ou envie um arquivo com o conteúdo do email.')
        return redirect(url_for('inicio'))

    texto_processado = preprocessar_texto(texto_email)
    categoria, pontuacao = analisar_email(texto_processado)

    chave_openai = os.environ.get('CHAVE_API_OPENAI', '').strip()
    if chave_openai:
        resposta_sugerida = gerar_resposta_openai(texto_email, categoria, chave_openai)
    else:
        if categoria == 'Produtivo':
            resposta_sugerida = (
                "Olá,\n\nRecebemos sua mensagem e estamos analisando o pedido. "
                "Encaminhei para o time responsável e retornaremos em até 2 dias úteis. "
                "Caso tenha informações adicionais, por favor responda este email.\n\nAtenciosamente,\nEquipe de Suporte"
            )
        else:
            resposta_sugerida = (
                "Olá,\n\nAgradecemos sua mensagem. Não é necessária nenhuma ação adicional no momento. "
                "Se precisar de suporte, abra um chamado através do portal.\n\nAtenciosamente,\nEquipe"
            )

    return render_template(
        'index.html',
        original_text=texto_email,
        category=categoria,
        score=pontuacao,
        suggested=resposta_sugerida
    )

if __name__ == '__main__':
    app.run(debug=True)
