import streamlit as st
from dataclasses import dataclass
from typing import Literal

from lib.utils.upload_arquivo import arquivoUpload
from lib.utils.converter_para_lista import converterParaLista

@dataclass
class Mensagem:
    origem: Literal["human", "ai"]
    mensagem: str

def iniciliazarValoresPadroes():
    if "historico_perguntas" not in st.session_state:
        st.session_state.historico_perguntas = []
    if "historico_respostas" not in st.session_state:
        st.session_state.historico_respostas = []
    if "indice" not in st.session_state:
        st.session_state.indice = 0
    if "pergunta_atual" not in st.session_state:
        st.session_state.pergunta_atual = None


def onSubmitCallback():
    usuario_resposta = st.session_state.usuario_resposta
    
    # Adiciona a resposta do usuário ao histórico de respostas
    st.session_state.historico_respostas.append(
        Mensagem('human', usuario_resposta)
    )
    
    # Se houver mais perguntas, avançar para a próxima pergunta
    if st.session_state.indice < len(st.session_state.perguntas)-1:
        st.session_state.indice += 1
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        texto = st.session_state.pergunta_atual['texto']
        
        # Adiciona a pergunta da IA ao histórico de perguntas
        st.session_state.historico_perguntas.append(
            Mensagem("ai", texto)
        )


iniciliazarValoresPadroes()
    
st.title("Bot")

json_dict = arquivoUpload()

if json_dict:
    perguntas = converterParaLista(json_dict)

    if "perguntas" not in st.session_state:
        st.session_state.perguntas = perguntas
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        
        # Adiciona a primeira pergunta da IA ao histórico de perguntas
        st.session_state.historico_perguntas.append(
            Mensagem("ai", st.session_state.pergunta_atual['texto'])
        )
    
    # Exibe apenas a pergunta atual
    st.write(f"Pergunta: {st.session_state.pergunta_atual['texto']}")

    # Exibe as respostas apenas para a pergunta atual
    pergunta_index = st.session_state.indice
    
    # Exibindo a pergunta
    with st.chat_message('assistant'):
        st.markdown(f"{st.session_state.pergunta_atual['texto']}")
    
    # Exibe as respostas correspondentes ao índice atual
    if pergunta_index < len(st.session_state.historico_respostas):
        with st.chat_message('human'):
            st.markdown(f"{st.session_state.historico_respostas[pergunta_index].mensagem}")
    
    # Caixa de entrada para o usuário responder
    prompt_placeholder = st.chat_input('Digite sua resposta', key='usuario_resposta' , on_submit=onSubmitCallback)
