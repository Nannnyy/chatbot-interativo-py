import streamlit as st
from lib.models.mensagem import Mensagem

def iniciliazarValoresPadroes():
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "indice" not in st.session_state:
        st.session_state.indice = 0
    if "pergunta_atual" not in st.session_state:
        st.session_state.pergunta_atual = None
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    if "arquivo_uploader" not in st.session_state:
        st.session_state.arquivo_uploader = True
    if "json_dict" not in st.session_state:
        st.session_state.json_dict = None
        
def onSubmitCallback():
    
    #Adicionar as perguntas e as respostas ao histórico
    
    #Resposta do usuário
    usuario_resposta = st.session_state.usuario_resposta
    st.session_state.historico.append(
        Mensagem('human', usuario_resposta)
    )
    
    
    #Verificar a resposta e enviar feedback
    if usuario_resposta.lower().strip() in st.session_state.pergunta_atual['resposta_correta'].lower().atrip():
        st.session_state.historico.append(
            Mensagem('feedback', 'Parabéns, você acertou')
        )
    else:
        st.session_state.historico.append(
        Mensagem('feedback', 'Poxa, você errou')
        )
    
    
    #Próxima pergunta
    
    st.session_state.indice += 1
    if st.session_state.indice < len(st.session_state.perguntas):
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        
        st.session_state.historico.append(
            Mensagem("ai", f"{st.session_state.pergunta_atual['id']}. {st.session_state.pergunta_atual['texto']}")
        )


def proximaPergunta():
    st.session_state.indice += 1
    if st.session_state.indice < len(st.session_state.perguntas):
        st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
        
        st.session_state.historico.append(
            Mensagem("ai", f"{st.session_state.pergunta_atual['id']}. {st.session_state.pergunta_atual['texto']}")
        )