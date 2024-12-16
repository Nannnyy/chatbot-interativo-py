import streamlit as st
import json

def arquivoUpload() -> dict:
    arquivo_uploaded = st.file_uploader('Escolha um arquivo', ['json'])
    
    if arquivo_uploaded:
        string_json = arquivo_uploaded.getvalue().decode('utf-8')
        json_dict = json.loads(string_json)
        return json_dict