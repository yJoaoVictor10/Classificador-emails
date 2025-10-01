# Classificador de Emails - Demo

Este projeto é uma aplicação web que permite classificar emails como **Produtivos** ou **Improdutivos**, utilizando Python, Flask e técnicas básicas de NLP (Natural Language Processing).  
Opcionalmente, também é possível gerar respostas automáticas usando **OpenAI**.

---

## Funcionalidades

- Classificação de emails com base em palavras-chave.
- Pré-processamento de texto: normalização, remoção de stopwords, stemming.
- Suporte a entrada de **texto direto** ou **upload de arquivos** (.txt ou .pdf).
- Geração de respostas automáticas:
  - Local (respostas simples baseadas na classificação).
  - Via OpenAI (usando chave de API).
- Interface web simples e amigável.

---

## Tecnologias Utilizadas

- **Python 3.13+**
- **Flask**
- **NLTK**
- **PyPDF2**
- **Werkzeug**
- **HTML / CSS / JS** (interface web)

---

## Instalação e Execução Local

1. **Clone o repositório**  
```bash
git clone <https://github.com/yJoaoVictor10/Classificador-emails.git>
cd AutoU-projeto
```

## Instalação e Execução Local

### 1. Ative o ambiente virtual (Windows PowerShell)
```bash
.\venv\Scripts\Activate.ps1
```

### 2. Crie um ambiente virtual (Windows PowerShell)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```


### 3. Crie um ambiente virtual (Windows CMD)
```bash
python -m venv venv
.\venv\Scripts\activate.bat
```

### 4. Crie um ambiente virtual (Linux/Mac)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Instalar dependências
```bash
pip install -r requirements.txt
```

### 6. Configurar variáveis de ambiente (opcional) (Linux/Mac)
```bash
export CHAVE_SECRETA_FLASK="uma_chave_secreta_segura"
export CHAVE_API_OPENAI="sua_chave_api_openai"
```

### 7. Configurar variáveis de ambiente (opcional) Windows (PowerShell)
```bash
$env:CHAVE_SECRETA_FLASK="uma_chave_secreta_segura"
$env:CHAVE_API_OPENAI="sua_chave_api_openai"
```

### 8. Executar a aplicação
```bash
python app.py
```
---
## 📝 Exemplos de Uso

- **Texto direto**: Cole o conteúdo do email no campo de texto e clique em **Analisar**.  
- **Upload de arquivo**: Selecione um arquivo `.txt` ou `.pdf` com o conteúdo do email.  
- **Chave OpenAI**: Insira sua chave para respostas geradas por IA.  

---

## 🔑 Dependências principais

- **Flask** – Backend web  
- **NLTK** – Processamento de linguagem natural  
- **PyPDF2** – Extração de texto de PDFs  
- **OpenAI** – Geração de respostas inteligentes *(opcional)*  

---

## 📌 Observações

- 🪟 Se for rodar no **Windows**, certifique-se de ativar corretamente o ambiente virtual antes de instalar as dependências.  
- 📂 A pasta **`/tmp/uploads`** será criada automaticamente para armazenar os arquivos enviados.  
- ☁️ Caso vá fazer **deploy**, pode ser necessário ajustar o caminho da pasta de uploads.  
