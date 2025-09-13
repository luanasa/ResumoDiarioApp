# **Resumo Diário **

Este projeto Python cria um agente automatizado que gera um resumo diário personalizado. Ele coleta as últimas notícias de várias fontes (agora incluindo sites que não têm RSS) e os trechos mais recentes dos seus e-mails do Gmail.

## **Funcionalidades**

* **Notícias de Fontes Variadas**: Captura manchetes tanto de fontes RSS quanto por meio de web scraping em sites populares como O Povo e Diário do Nordeste.  
* **Resumo de E-mails**: Conecta-se à sua conta do Gmail para pegar os snippets (trechos) dos e-mails mais recentes.  
* **Lista de Tarefas**: O resumo é gerado com checkboxes para que você possa acompanhar visualmente as notícias e e-mails que já revisou.  
* **Envio Automático por E-mail**: A ferramenta pode enviar o resumo diário diretamente para a sua caixa de entrada, facilitando o acesso ao conteúdo.

## **Como Usar**

### **1\. Instalação das dependências**

Certifique-se de que você tem o Python instalado e então instale as bibliotecas necessárias usando o pip:

pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib requests beautifulsoup4

### **2\. Configuração do Gmail API**

Para que o script acesse seus e-mails (para ler e enviar), você precisa de um arquivo de credenciais do Google Cloud.

1. Vá para o [Google Cloud Console](https://console.cloud.google.com/).  
2. Crie um novo projeto (ou selecione um existente).  
3. Vá em **APIs e Serviços** \> **Credenciais**.  
4. Clique em **Criar credenciais** e selecione **ID do cliente OAuth**.  
5. Configure a tela de consentimento OAuth, se ainda não o fez.  
6. Escolha o tipo de aplicativo "Desktop app".  
7. Baixe o arquivo JSON gerado e renomeie-o para credentials.json.  
8. Coloque o arquivo credentials.json na mesma pasta do seu script.

A primeira vez que você executar o script, ele abrirá uma janela do navegador para que você autorize o acesso à sua conta do Gmail. Um arquivo token.json será gerado automaticamente para futuras execuções.

### **3\. Execução do Script**

Após instalar as dependências e configurar o credentials.json, basta rodar o script a partir do terminal:

python seu\_script.py

O resumo diário será impresso no seu terminal e, se você configurar a função de envio, também será enviado para o e-mail que você definiu.

## **Personalização**

Você pode facilmente personalizar o agente:

* **Fontes de notícias**: Edite os dicionários fontes\_rss e noticias\_scraping na função agente\_resumo\_diario() para adicionar ou remover fontes.  
* **Número de itens**: Altere o valor do argumento limit nas funções get\_news\_rss(), get\_headlines\_diario\_do\_nordeste() e get\_headlines\_o\_povo() para pegar mais ou menos notícias/e-mails.  
* **E-mail de destino**: Dentro da função \_\_main\_\_, localize a linha meu\_email \= "seu\_email@gmail.com" e substitua pelo seu endereço de e-mail.

## **Estrutura do Projeto**

seu\_script.py  
credentials.json  
token.json (gerado automaticamente na primeira execução)  
