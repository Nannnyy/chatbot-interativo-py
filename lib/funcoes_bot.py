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
        #Limpar todo o session_state
        st.session_state.clear()
        #Recarregar a aplicação
        st.rerun() 


def mostrarPontuacao():
    # Exibe o subtítulo de forma separada
    st.subheader("Sua Pontuação final foi:")

    # Exibe a métrica com a pontuação
    st.metric(label="Pontuação", value=f"{st.session_state.score}/{len(st.session_state.perguntas)}")

def proximaPergunta():
    if st.session_state.indice < len(st.session_state.perguntas)-1:
        st.session_state.indice += 1
    else:
        st.session_state.terminar = True


def AtualizarResultadosQuiz():
    # Verifica se a resposta está correta
    resposta_correta = removerAcentos(st.session_state.resposta_atual.lower()).strip() == removerAcentos(st.session_state.pergunta_atual['resposta_correta'].lower()).strip()
    
    #Atribuir os valores da pergunta e resposta atuais para o resultado do quiz
    st.session_state.quiz_resultado.append({
        'id': st.session_state.pergunta_atual['id'],
        'texto': st.session_state.pergunta_atual['texto'],
        'resposta_usuario': st.session_state.resposta_atual,
        'pontos_adquiridos': 1 if resposta_correta else 0
    })
    
    # Incrementa a pontuação
    if resposta_correta:
        st.session_state.score += 1
        st.session_state.historico.append(
            Mensagem('feedback', f'🎉 Parabéns, você acertou', "success")
        )
    else:
        st.session_state.historico.append(
            Mensagem('feedback', f'❌ Poxa, você errou. Na verdade, a resposta é: {st.session_state.pergunta_atual['resposta_correta']}', "error")
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
        Mensagem('human', f"Resposta: {st.session_state.resposta_atual}", "")
    )
    
    #Atualizar os resultados
    AtualizarResultadosQuiz()
    
    #Incrementar para póxima pergunta
    proximaPergunta()






