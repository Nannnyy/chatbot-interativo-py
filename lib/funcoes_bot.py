import streamlit as st
from lib.models.mensagem import Mensagem
from lib.utils.remover_acento import removerAcentos

def inicializarValoresPadroes():
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "indice" not in st.session_state:
        st.session_state.indice = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "pergunta_atual" not in st.session_state:
        st.session_state.pergunta_atual = None
    if "resposta_atual" not in st.session_state:
        st.session_state.resposta_atual = None
    if "arquivo_uploader" not in st.session_state:
        st.session_state.arquivo_uploader = True
    if "json_dict" not in st.session_state:
        st.session_state.json_dict = None
    if "terminar" not in st.session_state:
        st.session_state.terminar = False
        
        
def restart():
    if st.button('Recomeçar'):
        st.session_state.clear()  # Limpar todo o session_state
        st.rerun()   # Recarregar a aplicação


def mostrarPontuacao():
    st.metric('Sua pontuação final foi:', f"{st.session_state.score}/{len(st.session_state.perguntas)}")


def proximaPergunta():
    if st.session_state.indice < len(st.session_state.perguntas)-1:
        st.session_state.indice += 1
    else:
        st.session_state.terminar = True


def corrigirResposta():
    if removerAcentos(
        st.session_state.resposta_atual.lower()
        ).strip() in removerAcentos(
            st.session_state.pergunta_atual['resposta_correta'].lower()).strip():
        #Incrementar pontuação
        st.session_state.score += 1
        
        # Feedback caso a resposta esteja correta
        st.session_state.historico.append(
            Mensagem('feedback', f'🎉 Parabéns, você acertou, pontuação atual: {st.session_state.score}')
        ) 
    else:
        #Feedback caso a resposta esteja errada
        st.session_state.historico.append(
        Mensagem('feedback', '❌ Poxa, você errou')
        )
       
        
def enviarResposta():
    #Adicionar as perguntas e as respostas ao histórico
    
    #Resposta do usuário
    usuario_resposta = st.session_state.usuario_resposta
    st.session_state.resposta_atual = usuario_resposta
    
    #Adicionar resposta ao histórico
    st.session_state.historico.append(
        Mensagem('human', st.session_state.resposta_atual)
    )
    
    # Corrigir a resposta
    corrigirResposta()
    
    #Incrementar para póxima pergunta
    proximaPergunta()





