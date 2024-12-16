class Mensagem:
    
    def __init__(self, origem, mensagem):
        self.origem = origem
        self.mensagem = mensagem
    
    def __repr__(self):
        return f"{self.mensagem}"
    
    def getOrigem(self):
        return self.origem
    
    def getMensagem(self):
        return self.mensagem