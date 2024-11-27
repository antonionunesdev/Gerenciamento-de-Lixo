from random import randint

class Ponto:
    def __init__(self, id):
        self.id = id
        self.quantidade_de_lixo = 0
        self.quantidade_de_gatos = 0
        self.quantidade_de_cachorros = 0
        self.quantidade_de_ratos = 0
        self.gerar_animais()


    def presença_do_animal(self, num_sorteado):  # define se há o animal no ponto com base na chance de sua presença
        if num_sorteado == 0: return 1
        return 0


    def gerar_animais(self):
        self.quantidade_de_ratos = self.presença_do_animal(randint(0,1))
        self.quantidade_de_gatos = self.presença_do_animal(randint(0,3))
        self.quantidade_de_cachorros = self.presença_do_animal(randint(0, 9))


    


    
