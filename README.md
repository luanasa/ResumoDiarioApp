# **🤖 Agente Resumo Diário**

### **Seu assistente pessoal para uma rotina mais informada.**

## **-> Sobre o Projeto**

Este projeto em Python cria um **agente de IA** que automatiza a geração de um resumo diário personalizado. Ele atua como um assistente inteligente, consolidando as informações mais relevantes do seu dia em um formato conciso e prático, enviado diretamente para o seu e-mail.

## **✨ Funcionalidades**

* **Notícias de Fontes Diversas**: 📰 Captura as manchetes mais recentes de portais de notícias como G1, O Povo e Diário do Nordeste, utilizando tanto feeds RSS quanto web scraping.  
* **Resumo de E-mails**: 📧 Conecta-se à sua conta do Gmail para extrair os trechos dos e-mails mais recentes, ajudando você a se manter atualizado.  
* **Lista de Pendências**: ✅ O resumo é gerado com checkboxes para que você possa acompanhar visualmente o que já revisou.  
* **Envio Automático por E-mail**: 🚀 O resumo diário é enviado para sua caixa de entrada, garantindo que as informações estejam sempre à mão.

## **-> Como Usar**

### **1\. Instalação**

Primeiro, clone o repositório e navegue até a pasta do projeto.

git clone \[https://github.com/seu-usuario/ResumoDiario.git\](https://github.com/seu-usuario/ResumoDiario.git)  
cd ResumoDiario

Em seguida, instale todas as bibliotecas necessárias:

pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib requests beautifulsoup4

### **2\. Configuração do Gmail API**

Para que o script acesse seus e-mails e possa enviá-los, é necessário um arquivo de credenciais do Google. Siga estes passos:

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).  
2. Crie ou selecione um projeto.  
3. Vá em **APIs e Serviços** \> **Credenciais**.  
4. Clique em **Criar credenciais** e selecione **ID do cliente OAuth**.  
5. Configure a tela de consentimento OAuth e escolha "Desktop app" como tipo de aplicativo.  
6. Baixe o arquivo JSON e salve-o como credentials.json na mesma pasta do seu script.

Na primeira execução, uma janela do navegador se abrirá para que você autorize o acesso à sua conta. Um arquivo token.json será gerado automaticamente.

### **3\. Execução**

Depois de instalar as dependências e configurar as credenciais, execute o script:

python seu\_script.py

O resumo será exibido no terminal e enviado para o e-mail que você definiu no código.

## **🛠️ Personalização**

Este agente foi feito para ser adaptável\! Você pode facilmente ajustá-lo para suas necessidades:

* **Fontes de notícias**: Edite as variáveis fontes\_rss e noticias\_scraping para adicionar ou remover suas fontes preferidas.  
* **Número de itens**: Altere o parâmetro limit nas funções de coleta para definir quantos itens (notícias ou e-mails) você quer no resumo.  
* **E-mail de destino**: Substitua "seu\_email@gmail.com" no código pelo seu próprio endereço de e-mail.

## **🤝 Contribuição**

Contribuições são bem-vindas\! Se você tiver ideias para novas funcionalidades ou melhorias, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## **📜 Licença**

Este projeto está sob a licença MIT. Para mais detalhes, consulte o arquivo LICENSE.
