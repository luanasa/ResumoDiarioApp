# **Resumo Diário**

Este projeto Python cria um agente automatizado que gera um resumo diário personalizado. Ele reúne as últimas notícias de várias fontes RSS e os trechos mais recentes dos seus e-mails do Gmail para apresentar uma visão geral rápida do que é importante no seu dia.

## **Funcionalidades**

* **Notícias de Fontes RSS**: Captura e lista as manchetes mais recentes de sites de notícias como G1, Diário do Nordeste e outros. As fontes são facilmente configuráveis no código.  
* **Resumo de E-mails**: Conecta-se à sua conta do Gmail para pegar os snippets (trechos) dos e-mails mais recentes.  
* **Lista de Tarefas**: O resumo é gerado com checkboxes para que você possa acompanhar visualmente as notícias e e-mails que já revisou.

## **Como Usar**

### **1\. Instalação das dependências**

Certifique-se de que você tem o Python instalado e então instale as bibliotecas necessárias usando o pip:

pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib

### **2\. Configuração do Gmail API**

Para que o script acesse seus e-mails, você precisa de um arquivo de credenciais do Google Cloud.

1. Vá para o [Google Cloud Console](https://console.cloud.google.com/).  
2. Crie um novo projeto (ou selecione um existente).  
3. Vá em **APIs e Serviços** \> **Credenciais**.  
4. Clique em **Criar credenciais** e selecione **ID do cliente OAuth**.  
5. Configure a tela de consentimento OAuth, se ainda não o fez.  
6. Escolha o tipo de aplicativo "Desktop app".  
7. Baixe o arquivo JSON gerado e renomeie-o para credentials.json.  
8. Coloque o arquivo credentials.json na mesma pasta do script resumo\_diario.py.

A primeira vez que você executar o script, ele abrirá uma janela do navegador para que você autorize o acesso à sua conta do Gmail. Um arquivo token.json será gerado automaticamente para futuras execuções.

### **3\. Execução do Script**

Após instalar as dependências e configurar o credentials.json, basta rodar o script a partir do terminal:

python resumo\_diario.py

O resumo diário será impresso diretamente no seu terminal.

## **Personalização**

Você pode facilmente personalizar o agente:

* **Fontes de notícias**: Edite o dicionário fontes na função agente\_resumo\_diario() para adicionar ou remover fontes RSS.  
* **Número de itens**: Altere o valor do argumento limit nas funções get\_news() e get\_emails() para pegar mais ou menos notícias/e-mails.

## **Estrutura do Projeto**

resumo\_diario.py  
credentials.json  
token.json (gerado automaticamente na primeira execução)  
