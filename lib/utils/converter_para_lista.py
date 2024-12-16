def converterParaLista(json_dict: dict) -> list[dict]:
    perguntas = []
    
    for pergunta in json_dict["perguntas"]:
        perguntas.append(pergunta)
    
    return perguntas