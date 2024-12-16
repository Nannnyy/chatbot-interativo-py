import streamlit as st
import json

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
    if "quiz_resultado" not in st.session_state:
        st.session_state.quiz_resultado = []
        
        
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


# def corrigirResposta():
#     if removerAcentos(
#         st.session_state.resposta_atual.lower()
#         ).strip() in removerAcentos(
#             st.session_state.pergunta_atual['resposta_correta'].lower()).strip():
#         #Incrementar pontuação
#         st.session_state.score += 1
        
#         # Feedback caso a resposta esteja correta
#         st.session_state.historico.append(
#             Mensagem('feedback', f'🎉 Parabéns, você acertou, pontuação atual: {st.session_state.score}')
#         ) 
#     else:
#         #Feedback caso a resposta esteja errada
#         st.session_state.historico.append(
#         Mensagem('feedback', '❌ Poxa, você errou')
#         )

def AtualizarResultadosQuiz():
    # Verifica se a resposta está correta
    resposta_correta = removerAcentos(st.session_state.resposta_atual.lower()).strip() == removerAcentos(st.session_state.pergunta_atual['resposta_correta'].lower()).strip()
    
    st.session_state.quiz_resultado.append({
        'id': st.session_state.pergunta_atual['id'],
        'texto': st.session_state.pergunta_atual['texto'],
        'resposta_usuario': st.session_state.resposta_atual,
        'pontos_adquiridos': 1 if resposta_correta else 0
    })
    
    # Incrementa a pontuação apenas aqui
    if resposta_correta:
        st.session_state.score += 1
        st.session_state.historico.append(
            Mensagem('feedback', f'🎉 Parabéns, você acertou, pontuação atual: {st.session_state.score}')
        )
    else:
        st.session_state.historico.append(
            Mensagem('feedback', '❌ Poxa, você errou')
        )

def gerarArquivoJson():
    
    json_data = {
        'quiz_results': st.session_state.quiz_resultado,
        'pontuacao_final': st.session_state.score
    }
    
    return json.dumps(json_data, indent=4)
        
def enviarResposta():
    #Adicionar as perguntas e as respostas ao histórico
    
    #Resposta do usuário
    usuario_resposta = st.session_state.usuario_resposta
    st.session_state.resposta_atual = usuario_resposta
    
    #Adicionar resposta ao histórico
    st.session_state.historico.append(
        Mensagem('human', st.session_state.resposta_atual)
    )
    
    #Adicionar ao arquivo json
    AtualizarResultadosQuiz()
    
    # Corrigir a resposta
   
    
    #Incrementar para póxima pergunta
    proximaPergunta()






