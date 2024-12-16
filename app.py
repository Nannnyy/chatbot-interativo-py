
def app():
        
    # Iniciar os valores padrões do session_state
    inicializarValoresPadroes()
    
    
    #Título
    st.title("Bot")

    if st.session_state.arquivo_uploader:
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
                Mensagem( "ai", f"{st.session_state.pergunta_atual['id']}. {st.session_state.pergunta_atual['texto']}")            )
            
            chat_palceholder = st.container()
            resposta_placeholder = st.container(border=True)
            
            
            if st.session_state.pergunta_atual['tipo'] == 'multipla_escolha':
                        resposta_placeholder = st.radio(
                        "Escolha uma opção:",
                        options=st.session_state.pergunta_atual['opcoes'], 
                        key='usuario_resposta',
                        index=None,
                        on_change=enviarResposta
                        )
                        
            elif st.session_state.pergunta_atual['tipo'] == 'verdadeiro_falso':
                    resposta_placeholder = st.radio(
                        "Escolha uma opção:",
                        options=['Verdadeiro', 'Falso'], 
                        key='usuario_resposta',
                        index=None,
                        on_change=enviarResposta
                        )
            else:
                    #Espaço para usuário responder     
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
                        with st.chat_message('assistant', avatar="❓"):
                            st.markdown(mensagem)
                                
                    #Para feedback
                    elif mensagem.getOrigem() == "feedback":
                        with st.chat_message('assistant'):
                            st.markdown(mensagem)
                                
                    #Para resposta
                    else:
                        with st.chat_message('human'):
                            st.markdown(mensagem)
            
              
              
        #Acabar o jogo
        else:
            st.subheader("🏆 jogo ja foi finalizado!")
            mostrarPontuacao()
            restart()



if __name__ == "__main__":
    import streamlit as st

    from lib.utils.upload_arquivo import arquivoUpload
    from lib.utils.converter_para_lista import converterParaLista
    from lib.models.mensagem import Mensagem
    from lib.funcoes_bot import *

    app()