class Mensagem:
    
    def __init__(self, origem, mensagem, tipo):
        self.origem = origem
        self.mensagem = mensagem
        self.tipo = tipo
    
    def __repr__(self):
        return f"{self.mensagem}"
    
    def getOrigem(self):
        return self.origem
    
    def getMensagem(self):
        return self.mensagem
    
    def getTipo(self):
        return self.tipo