# Quiz Chatbot

Este projeto é um **chatbot de quiz** desenvolvido utilizando **Streamlit**, que permite aos usuários fazerem upload de um arquivo JSON contendo perguntas para realizar um quiz interativo. O chatbot vai guiá-los pelas perguntas, fornecendo feedback sobre as respostas e apresentando a pontuação final no término do quiz.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos:

- `app.py`: O script principal que executa a aplicação.
- `lib/`: Pasta contendo funções auxiliares, como o upload do arquivo JSON e conversão para lista.
- ´lib/funcoes_bot`: Lista de todas as funções que o bot pode realizar
- `lib/static/style.css`: Arquivo CSS para personalizar o estilo da aplicação.
- `README.md`: Este arquivo, contendo informações sobre como rodar o projeto.

Para o projeto funcionar, deve se utilizar um arquivo JSON com a seguinte estrutura:

<pre> ```json { "perguntas": [ { "id": 1, "texto": "Qual é a capital da França?", "tipo": "aberta", "resposta_correta": "Paris" }, { "id": 2, "texto": "Quem pintou a 'Mona Lisa'?", "tipo": "aberta", "resposta_correta": "Leonardo Da Vinci" }, { "id": 3, "texto": "Em que ano o homem pisou na Lua pela primeira vez?", "tipo": "aberta", "resposta_correta": "1969" }, { "id": 4, "texto": "Qual é o resultado de 3 + 2?", "tipo": "aberta", "resposta_correta": "5" }, { "id": 5, "texto": "Java é uma linguagem de programação.", "tipo": "verdadeiro_falso", "resposta_correta": "verdadeiro" }, { "id": 6, "texto": "Qual é a maior cidade do Brasil?", "tipo": "multipla_escolha", "opcoes": ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília"], "resposta_correta": "São Paulo" } ] } ``` </pre>

## Requisitos

- Python 3.x
- Streamlit

## Instalação e Execução

1. Clone este repositório em seu ambiente local:

   ```bash
   git clone https://github.com/Nannnyy/quiz-chatbot.git
