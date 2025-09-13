# -----------------------------
# Instalação das bibliotecas
# -----------------------------
# !pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib requests beautifulsoup4

import feedparser
from datetime import date
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
import base64
import os
import requests
from bs4 import BeautifulSoup

# -----------------------------
# Escopos da API
# -----------------------------
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

# -----------------------------
# Função: Obter credenciais
# -----------------------------
def get_credentials():
    if not os.path.exists("token.json"):
        if not os.path.exists("credentials.json"):
            print("❌ credentials.json não encontrado. Gere no Google Cloud Console.")
            return None
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        print("✅ token.json gerado com sucesso!")
    else:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return creds

# -----------------------------
# Função: Capturar notícias via RSS com links
# -----------------------------
def get_news_rss(sources, limit=5):
    noticias = {}
    for nome, url in sources.items():
        feed = feedparser.parse(url)
        manchetes = []
        for entry in feed.entries[:limit]:
            link = entry.link
            title = entry.title
            manchetes.append((title, link))
        noticias[nome] = manchetes
    return noticias

# -----------------------------
# Função: Scraping para sites sem RSS com links
# -----------------------------
def get_headlines_diario_do_nordeste(limit=5):
    url = "https://diariodonordeste.verdesmares.com.br/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = []
    for h in soup.find_all("h2")[:limit]:
        a_tag = h.find("a")
        if a_tag:
            headlines.append((a_tag.get_text(strip=True), a_tag.get("href")))
    return headlines

def get_headlines_o_povo(limit=5):
    url = "https://www.opovo.com.br/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = []
    for h in soup.find_all("h2")[:limit]:
        a_tag = h.find("a")
        if a_tag:
            headlines.append((a_tag.get_text(strip=True), a_tag.get("href")))
    return headlines

# -----------------------------
# Função: Capturar e-mails via Gmail API
# -----------------------------
def get_emails(creds, limit=10):
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=limit).execute()
    messages = results.get("messages", [])

    email_list = []
    for msg in messages:
        txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = txt.get("snippet", "")
        email_list.append(snippet)
    return email_list

# -----------------------------
# Função: Detectar pendências nos e-mails
# -----------------------------
def detectar_pendencias(emails):
    pendencias = []
    palavras_chave = ["pendência", "tarefa", "prazo", "entregar", "agendar", "reunião", "revisar", "atualizar"]
    for email in emails:
        for palavra in palavras_chave:
            if palavra.lower() in email.lower() and email not in pendencias:
                pendencias.append(email)
    return pendencias

# -----------------------------
# Função: Criar o resumo diário em HTML
# -----------------------------
def agente_resumo_diario(creds):
    # RSS
    fontes_rss = {
        "G1": "https://g1.globo.com/rss/g1/"
    }
    noticias_rss = get_news_rss(fontes_rss)

    # Scraping
    noticias_scraping = {
        "Diário do Nordeste": get_headlines_diario_do_nordeste(),
        "O Povo": get_headlines_o_povo()
    }

    emails = get_emails(creds)
    pendencias = detectar_pendencias(emails)

    # HTML do resumo
    resumo_html = f"<h2>✅ Resumo Diário – {date.today().strftime('%d/%m/%Y')}</h2>"

    # Notícias RSS
    resumo_html += "<h3>📌 Notícias (RSS)</h3>"
    for fonte, items in noticias_rss.items():
        resumo_html += f"<b>{fonte}</b><ul>"
        for title, link in items:
            resumo_html += f'<li><a href="{link}">{title}</a></li>'
        resumo_html += "</ul>"

    # Notícias Scraping
    resumo_html += "<h3>📌 Notícias (Websites)</h3>"
    for fonte, items in noticias_scraping.items():
        resumo_html += f"<b>{fonte}</b><ul>"
        for title, link in items:
            resumo_html += f'<li><a href="{link}">{title}</a></li>'
        resumo_html += "</ul>"

    # E-mails
    resumo_html += "<h3>📌 E-mails</h3><ul>"
    for item in emails:
        resumo_html += f"<li>{item}</li>"
    resumo_html += "</ul>"

    # Pendências inteligentes
    resumo_html += "<h3>📌 Pendências identificadas</h3><ul>"
    if pendencias:
        for p in pendencias:
            resumo_html += f"<li>{p}</li>"
    else:
        resumo_html += "<li>Sem pendências detectadas</li>"
    resumo_html += "</ul>"

    return resumo_html

# -----------------------------
# Função: Enviar e-mail via Gmail API (HTML)
# -----------------------------
def enviar_email(creds, destinatario, assunto, corpo_html):
    service = build("gmail", "v1", credentials=creds)
    mensagem = MIMEText(corpo_html, 'html')
    mensagem['to'] = destinatario
    mensagem['from'] = destinatario
    mensagem['subject'] = assunto

    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()
    body = {'raw': raw}

    service.users().messages().send(userId="me", body=body).execute()
    print(f"✅ E-mail enviado para {destinatario} com sucesso!")

# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    creds = get_credentials()
    if creds:
        resumo_html = agente_resumo_diario(creds)
        print(resumo_html)

        # Enviar para você mesmo
        meu_email = "seuemail@gmail.com"  # substitua pelo seu e-mail
        enviar_email(creds, meu_email, f"Resumo Diário – {date.today().strftime('%d/%m/%Y')}", resumo_html)
