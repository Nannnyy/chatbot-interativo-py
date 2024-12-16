
def app():
    
    st.markdown(
        """
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        </html>
        """, unsafe_allow_html=True
    )
    
    #Carregar os estilos
    carregarCss("lib/static/style.css")
    
    # Iniciar os valores padrões do session_state
    inicializarValoresPadroes()
    
    
    #Título
    st.title("Bem-vindo ao Chatbot 🤖")
    st.write("")


    #Uploader do arquivo json
    if st.session_state.arquivo_uploader:
        with st.container(border=True):
            st.markdown(
                """
                <div class="instrucoes">
                    INSTRUÇÕES: <br>
                    - Para começar, faça o upload de um arquivo JSON. O chat começará automaticamente após o upload. <br>
                    - O chat contém diferentes tipos de perguntas, como: abertas, verdadeiras ou falsas, e múltiplas opções. Fique atento ao tipo de pergunta antes de responder. <br>
                    - As respostas são corrigidas sem levar em consideração a pontuação e sem diferenciar entre maiúsculas e minúsculas. Portanto, não se preocupe com o formato da sua resposta. <br>
                    - Ao final do quiz, sua pontuação será revelada e você poderá baixar um arquivo JSON com seus resultados. 
                </div>
                
                """,
                unsafe_allow_html=True
            )
        st.write("")
        st.session_state.json_dict = arquivoUpload()


    if st.session_state.json_dict is not None:
        st.session_state.arquivo_uploader = False
        
        perguntas = converterParaLista(st.session_state.json_dict)

        #Adicionar a lista de perguntas
        if "perguntas" not in st.session_state:
            st.session_state.perguntas = perguntas
            #Atualização para esconder o file uploader
            st.rerun()
           
            
        #Começar o jogo
        if st.session_state.terminar == False: 
            
            #Atualizar a pergunta_atual
            st.session_state.pergunta_atual = st.session_state.perguntas[st.session_state.indice]
            
            #Adicionar pergunta atual ao historico
            st.session_state.historico.append(
                Mensagem( "ai", f"{st.session_state.pergunta_atual['id']}. {st.session_state.pergunta_atual['texto']}", "")            )
            
            chat_palceholder = st.container()
            resposta_placeholder = st.container(border=True)
            
            
            if st.session_state.pergunta_atual['tipo'] == 'multipla_escolha':
                
                st.markdown("""
                    <div class="radio-container">
                        <h4>Escolha uma opção:</h4>
                        <div class="radio-group">
                            <!-- Placeholder para Streamlit radio -->
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                resposta_placeholder = st.radio(
                    label="Escolha uma opção:",
                    options=st.session_state.pergunta_atual['opcoes'],
                    key='usuario_resposta',
                    index=None,
                    on_change=enviarResposta,
                    label_visibility="collapsed" 
                )
                        
            elif st.session_state.pergunta_atual['tipo'] == 'verdadeiro_falso':
        
                st.markdown("""
                    <div class="radio-container">
                        <h4>Escolha uma opção:</h4>
                        <div class="radio-group">
                            <!-- Placeholder para Streamlit radio -->
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                    
                resposta_placeholder = st.radio(
                    "Escolha uma opção:",
                    options=['Verdadeiro', 'Falso'], 
                    key='usuario_resposta',
                    index=None,
                    on_change=enviarResposta,
                    label_visibility="collapsed"
                )
                
            else:
  
                resposta_placeholder = st.chat_input(
                    'Digite sua resposta', 
                    key='usuario_resposta' , 
                    on_submit=enviarResposta
                )
            
            with chat_palceholder:
                #Mostrar as perguntas,respostas e feedbacks adicionados ao historico     
                for mensagem in st.session_state.historico:
                        
                    #Para pergunta
                    if mensagem.getOrigem() == "ai":
                        with st.chat_message(avatar="❓", name="ai"):
                            st.markdown(mensagem)
                                
                    #Para feedback
                    elif mensagem.getOrigem() == "feedback":
                        if mensagem.getTipo() == "success":
                            st.success(mensagem)
                        elif mensagem.getTipo() == "error":
                            st.error(mensagem)
                                
                    #Para resposta
                    else:
                            div = f"""
                            <div class="chat-row row-reverse">
                                <div class="chat-message">{mensagem}</div>
                                <div class="chat-icon">👤</div>
                            </div>
                            """
                            st.markdown(div, unsafe_allow_html=True)
                    st.write("")
            
              
              
        #Acabar o jogo
        else:
            st.header("🏆 jogo ja foi finalizado!")
            st.write("")
            mostrarPontuacao()
            st.write("")
            json_result = gerarArquivoJson()
            st.download_button(
                label="Baixar resultados do quiz",
                data=json_result,
                file_name="quiz_resultados.json",
                mime="application/json"
            )
            st.write("")
            restart()

def carregarCss(caminho_css):
    with open(caminho_css, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    import streamlit as st

    from lib.utils.upload_arquivo import arquivoUpload
    from lib.utils.converter_para_lista import converterParaLista
    from lib.models.mensagem import Mensagem
    from lib.funcoes_bot import *

    app()