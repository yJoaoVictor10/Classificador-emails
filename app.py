from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from classifier import analyze_email, preprocess_text, generate_response_with_openai, extract_text_from_file

# Diretório temporário para uploads no serverless Vercel
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'troque_para_uma_chave_secreta_real')

# Cria a pasta temporária, se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    email_text = request.form.get('email_text', '').strip()

    # Verifica se o usuário enviou arquivo
    if 'email_file' in request.files and request.files['email_file'].filename != '':
        file = request.files['email_file']
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Extrai o texto do arquivo (PDF ou TXT)
            email_text = extract_text_from_file(file_path)
        else:
            flash('Formato de arquivo não permitido. Use apenas .txt ou .pdf')
            return redirect(url_for('index'))

    if not email_text:
        flash('Por favor, insira um texto ou envie um arquivo com o conteúdo do email.')
        return redirect(url_for('index'))

    processed_text = preprocess_text(email_text)
    category, score = analyze_email(processed_text)

    # Usa variável de ambiente para OpenAI
    openai_key = os.environ.get('OPENAI_API_KEY', '').strip()
    if openai_key:
        suggested_reply = generate_response_with_openai(email_text, category, openai_key)
    else:
        if category == 'Produtivo':
            suggested_reply = (
                "Olá,\n\nRecebemos sua mensagem e estamos analisando o pedido. "
                "Encaminhei para o time responsável e retornaremos em até 2 dias úteis. "
                "Caso tenha informações adicionais, por favor responda este email.\n\nAtenciosamente,\nEquipe de Suporte"
            )
        else:
            suggested_reply = (
                "Olá,\n\nAgradecemos sua mensagem. Não é necessária nenhuma ação adicional no momento. "
                "Se precisar de suporte, abra um chamado através do portal.\n\nAtenciosamente,\nEquipe"
            )

    return render_template(
        'index.html',
        original_text=email_text,
        category=category,
        score=score,
        suggested=suggested_reply
    )

# NUNCA chame app.run() no serverless
# Vercel cuidará de iniciar a app automaticamente
