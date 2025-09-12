# -----------------------------
# Instalação das bibliotecas
# -----------------------------
# !pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib

import feedparser
from datetime import date
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

    # Se token.json não existir, cria automaticamente
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
# Função: Agente de Resumo Diário
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

    # Pendências detectadas (exemplo)
    resumo += "📌 Pendências identificadas\n"
    resumo += "- [ ] Criar apresentação para reunião de sexta.\n"
    resumo += "- [ ] Revisar gastos da semana no financeiro.\n"

    return resumo

# -----------------------------
# Execução
# -----------------------------
if __name__ == "__main__":
    print(agente_resumo_diario())
