import streamlit as st

from lib.utils.upload_arquivo import arquivoUpload
from lib.utils.converter_para_lista import converterParaLista
from lib.models.mensagem import Mensagem


def iniciliazarValoresPadroes():
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "historico_perguntas" not in st.session_state:
        st.session_state.historico_perguntas = []
    if "historico_respostas" not in st.session_state:
        st.session_state.historico_respostas = []
    if "indice" not in st.session_state:
        st.session_state.indice = 0
    if "pergunta_atual" not in st.session_state:
        st.session_state.pergunta_atual = None


def onSubmitCallback():
    #Adicionar as perguntas e as respostas ao histórico
    usuario_resposta = st.session_state.usuario_resposta
    
    st.session_state.historico.append(
        Mensagem('human', usuario_resposta)
    )
    
    st.session_state.indice += 1
    if st.session_state.indice < len(st.session_state.perguntas):
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        texto = st.session_state.pergunta_atual['texto']
        
        st.session_state.historico.append(
            Mensagem("ai", st.session_state.pergunta_atual['texto'])
        )

# Iniciar os valores padrões do session_state
iniciliazarValoresPadroes()

#Título
st.title("Bot")

#Carregar o arquivo
json_dict = arquivoUpload()

if json_dict:
    
    perguntas = converterParaLista(json_dict)

    #Adicionar a lista de perguntas
    if "perguntas" not in st.session_state:
        st.session_state.perguntas = perguntas
        
        #Criar a primeira pergunta
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        
        #Adicionar a primeira pergunta ao histórico
        st.session_state.historico.append(
            Mensagem("ai", st.session_state.pergunta_atual['texto'])
        )


    chat_placeholder = st.container()

    #Começar o jogo
    if st.session_state.indice < len(st.session_state.perguntas):     
        
        #Espaço para usuário responder     
        prompt_placeholder = st.chat_input('Digite sua resposta', key='usuario_resposta' , on_submit=onSubmitCallback)
        
        #Mostrar as perguntas e respostas
        with chat_placeholder:
            for chat in st.session_state.historico:
                with st.chat_message('assistant'):
                    st.markdown(f"{chat.origem}: {chat.mensagem}")
                    
    #Acabar o jogo
    else:
        st.markdown("Nossa, o jogo ja acabou")