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
# Função: Capturar notícias via RSS
# -----------------------------
def get_news_rss(sources, limit=5):
    noticias = {}
    for nome, url in sources.items():
        feed = feedparser.parse(url)
        manchetes = [entry.title for entry in feed.entries[:limit]]
        noticias[nome] = manchetes
    return noticias

# -----------------------------
# Função: Scraping para sites sem RSS
# -----------------------------
def get_headlines_diario_do_nordeste(limit=5):
    url = "https://diariodonordeste.verdesmares.com.br/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = [h.get_text(strip=True) for h in soup.find_all("h2")[:limit]]
    return headlines

def get_headlines_o_povo(limit=5):
    url = "https://www.opovo.com.br/"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = [h.get_text(strip=True) for h in soup.find_all("h2")[:limit]]
    return headlines

# -----------------------------
# Função: Capturar e-mails via Gmail API
# -----------------------------
def get_emails(creds, limit=3):
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
# Função: Criar o resumo diário
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

    resumo = f"✅ Resumo Diário – {date.today().strftime('%d/%m/%Y')}\n\n"

    # Notícias RSS
    resumo += "📌 Notícias (RSS)\n"
    for fonte, manchetes in noticias_rss.items():
        resumo += f"🔹 {fonte}\n"
        for item in manchetes:
            resumo += f"- [ ] {item}\n"
        resumo += "\n"

    # Notícias Scraping
    resumo += "📌 Notícias (Websites)\n"
    for fonte, manchetes in noticias_scraping.items():
        resumo += f"🔹 {fonte}\n"
        for item in manchetes:
            resumo += f"- [ ] {item}\n"
        resumo += "\n"

    # E-mails
    resumo += "📌 E-mails\n"
    for item in emails:
        resumo += f"- [ ] {item}\n"
    resumo += "\n"

    # Pendências
    resumo += "📌 Pendências identificadas\n"
    resumo += "- [ ] Criar apresentação para reunião de sexta.\n"
    resumo += "- [ ] Revisar gastos da semana no financeiro.\n"

    return resumo

# -----------------------------
# Função: Enviar e-mail via Gmail API
# -----------------------------
def enviar_email(creds, destinatario, assunto, corpo):
    service = build("gmail", "v1", credentials=creds)
    mensagem = MIMEText(corpo)
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
        resumo = agente_resumo_diario(creds)
        print(resumo)

        # Enviar para você mesmo
        meu_email = "seu_email@gmail.com"  # substitua pelo seu e-mail
        enviar_email(creds, meu_email, f"Resumo Diário – {date.today().strftime('%d/%m/%Y')}", resumo)
