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
git clone <URL_DO_REPOSITORIO>
cd AutoU-projeto
```

## Instalação e Execução Local

### 1. Ative o ambiente virtual (Windows PowerShell)
```bash
.\venv\Scripts\Activate.ps1
```

### 1. Crie um ambiente virtual
```bash
python -m venv venv
```
