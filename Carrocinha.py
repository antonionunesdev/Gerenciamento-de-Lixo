class Carrocinha:
    def __init__(self, bairro):
        self.bairro = bairro
        self.capacidade = 5
        self.animais_transportados = 0
        self.tempo_gasto = 0
        self.ponto_atual = self.bairro.zoonoses

    def recolher_animais(self):
        # calcula para cachorros e gatos, a possibilidade de se transportar todos os presentes
        # no local, ou se alguns deles já enchem a carrocinha.
        cachorros_recolhidos = min(
            self.ponto_atual.quantidade_de_cachorros, self.capacidade - self.animais_transportados
        )
        self.animais_transportados += cachorros_recolhidos
        self.ponto_atual.quantidade_cachorros -= cachorros_recolhidos

        gatos_recolhidos = min(
            self.ponto_atual.quantidade_de_gatos, self.capacidade - self.animais_transportados
        )
        self.animais_transportados += gatos_recolhidos
        self.ponto_atual.quantidade__de_gatos -= gatos_recolhidos


    def retornar_ao_centro(self):
        # é chamada exatamente quando a carrocinha fica cheia
        tempo_de_retorno, caminho = self.bairro.djikstra(self.ponto_atual, self.bairro.zoonoses)
        self.tempo_gasto += tempo_de_retorno
        self.animais_transportados = 0


    def iniciar_rota(self, destino):
        # é chamada assim que se recebe um alerta de presença de animal
        tempo_total_gasto, caminho = self.bairro.djikstra(self.ponto_atual, destino)
        for i in range(1, len(caminho)):
            if self.animais_transportados == self.capacidade:
                # capacidade máxima atingida durante o percurso
                self.retornar_ao_centro()
                break
            for vizinho, peso in self.bairro.adjacencicas[caminho[i-1]]:
                # calculando o tempo gasto de um ponto ao vizinho
                if vizinho == caminho[i]:
                    self.tempo_gasto += peso
                    break
            self.ponto_atual = caminho[i]
            self.recolher_animais()
        # caso se recolha os animais no ponto solicitado e a carrocinha continue com capacidade, 
        # ela permanece nesse ponto esperando uma nova solicitação
