# -----------------------------
# Instalação das bibliotecas
# -----------------------------
# !pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib

import feedparser
from datetime import date
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
import base64
import os

# -----------------------------
# Função: Capturar notícias via RSS
# -----------------------------
def get_news(sources, limit=3):
    noticias = {}
    for nome, url in sources.items():
        feed = feedparser.parse(url)
        manchetes = [entry.title for entry in feed.entries[:limit]]
        noticias[nome] = manchetes
    return noticias

# -----------------------------
# Função: Capturar e-mails via Gmail API
# -----------------------------
def get_emails(limit=3):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    if not os.path.exists("token.json"):
        if not os.path.exists("credentials.json"):
            print("❌ credentials.json não encontrado. Gere no Google Cloud Console.")
            return ["Erro: credentials.json não encontrado"]
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        print("✅ token.json gerado com sucesso!")
    else:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

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
def agente_resumo_diario():
    fontes = {
        "The News": "https://thenewscc.com.br/feed/",
        "G1": "https://g1.globo.com/rss/g1/",
        "Diário do Nordeste": "https://diariodonordeste.verdesmares.com.br/rss",
        "O Povo": "https://www.opovo.com.br/rss.xml"
    }

    noticias = get_news(fontes)
    emails = get_emails()

    resumo = f"✅ Resumo Diário – {date.today().strftime('%d/%m/%Y')}\n\n"

    # Notícias
    resumo += "📌 Notícias\n"
    for fonte, manchetes in noticias.items():
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
def enviar_email(destinatario, assunto, corpo):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    if not os.path.exists("token.json"):
        print("❌ token.json não encontrado para enviar e-mail. Gere usando OAuth.")
        return

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # Criar a mensagem MIME
    mensagem = MIMEText(corpo)
    mensagem['to'] = destinatario
    mensagem['from'] = destinatario
    mensagem['subject'] = assunto

    # Codificar mensagem em base64
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()
    body = {'raw': raw}

    # Enviar
    service.users().messages().send(userId="me", body=body).execute()
    print(f"✅ E-mail enviado para {destinatario} com sucesso!")

# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    resumo = agente_resumo_diario()
    print(resumo)

    # Enviar para você mesmo
    meu_email = "seu_email@gmail.com"  # substitua pelo seu e-mail
    enviar_email(meu_email, f"Resumo Diário – {date.today().strftime('%d/%m/%Y')}", resumo)
