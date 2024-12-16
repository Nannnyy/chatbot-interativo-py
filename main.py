import streamlit as st

from lib.utils.upload_arquivo import arquivoUpload
from lib.utils.converter_para_lista import converterParaLista
from lib.models.mensagem import Mensagem
from lib.funcoes_bot import *

def main():
    # Iniciar os valores padrões do session_state
    inicializarValoresPadroes()
    
    # Título
    st.title("Bot")

    if st.session_state.arquivo_uploader:
        st.session_state.json_dict = arquivoUpload()

    if st.session_state.json_dict is not None:
        st.session_state.arquivo_uploader = False
        perguntas = converterParaLista(st.session_state.json_dict)

        # Adicionar a lista de perguntas
        if "perguntas" not in st.session_state:
            st.session_state.perguntas = perguntas
            st.rerun()

        # Mostrar as mensagens do histórico
        for mensagem in st.session_state.historico:
            if mensagem.getOrigem() == "ai":
                with st.chat_message('assistant', avatar="❓"):
                    st.markdown(mensagem)
            elif mensagem.getOrigem() == "feedback":
                with st.chat_message('assistant'):
                    st.markdown(mensagem)
            else:
                with st.chat_message('human'):
                    st.markdown(mensagem)

        # Lógica para determinar se o jogo acabou
        if st.session_state.terminar:
            st.subheader("🏆 O jogo foi finalizado!")
            mostrarPontuacao()
            restart()
        else:
            # Obter a pergunta atual
            pergunta_atual = st.session_state.perguntas[st.session_state.indice]
            st.session_state.pergunta_atual = pergunta_atual

            # Adicionar pergunta ao histórico apenas uma vez
            if len(st.session_state.historico) == 0 or st.session_state.historico[-1].getOrigem() != "ai":
                st.session_state.historico.append(
                    Mensagem("ai", f"{pergunta_atual['id']}. {pergunta_atual['texto']}")
                )

            # Tipo da pergunta
            tipo = pergunta_atual['tipo']

            # Formas de resposta baseadas no tipo da pergunta
            if tipo == "aberta":
                resposta_usuario = st.chat_input("Digite sua resposta", key="usuario_resposta")
                if resposta_usuario:
                    enviarResposta(resposta_usuario)

            elif tipo == "verdadeiro_falso":
                resposta_usuario = st.radio(
                    "Escolha uma opção:", 
                    options=["Verdadeiro", "Falso"], 
                    key=f"radio_{st.session_state.indice}"
                )
                if resposta_usuario:
                    enviarResposta(resposta_usuario)

            elif tipo == "multipla_escolha":
                opcoes = pergunta_atual.get("opcoes", [])
                resposta_usuario = st.radio(
                    "Escolha a alternativa correta:", 
                    options=opcoes, 
                    key=f"radio_{st.session_state.indice}"
                )
                if resposta_usuario:
                    enviarResposta(resposta_usuario)

main()