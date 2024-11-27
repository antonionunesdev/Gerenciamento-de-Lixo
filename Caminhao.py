class Caminhao:
    def __init__(self, bairro, num_funcionarios):
        self.bairro = bairro
        self.num_funcionarios = num_funcionarios
        self.capacidade_total = 100
        self.capacidade_restante = 100
        self.ponto_atual = bairro.aterro
        self.tempo_gasto = 0


    def coletar_lixo(self):
        if self.ponto_atual.quantidade_de_ratos > 0 or self.ponto_atual.quantidade_de_gatos > 0 or self.ponto_atual.quantidade_de_cachorros > 0:
            lixo_espalhado = True
            self.solicitar_carrocinha()
            
        if self.capacidade_restante >= self.ponto_atual.quantidade_lixo: 
            tempo = self.ponto_atual.quantidade_lixo / self.num_funcionarios
            self.capacidade_restante -= self.ponto_atual.quantidade_lixo
            self.ponto_atual.quantidade_lixo = 0
        else:
            tempo = self.capacidade_restante / self.num_funcionarios
            self.capacidade_restante = 0
            self.ponto_atual.quantidade_lixo -= self.capacidade_restante
        if lixo_espalhado:
            tempo *= 2
        self.tempo_gasto += tempo
        

    def retornar_ao_aterro(self):
        self.capacidade_restante = self.capacidade_total
        self.tempo_gasto += self.bairro.djikstra(self.ponto_atual, self.bairro.aterro)
        self.ponto_atual = self.bairro.aterro


    def sessao_de_coleta(self):
        while self.capacidade_restante > 0 and self.bairro.tem_pontos_sujos():
            self.proximo_ponto_de_coleta()
            self.coletar_lixo()
        self.retornar_ao_aterro()


    def proximo_ponto_de_coleta(self):
        pontos_sujos = []
        for ponto in self.bairro:
            if ponto.quantidade_lixo > 0:
                pontos_sujos.append(ponto)

        min_caminho = self.bairro.djikstra(self.ponto_atual, pontos_sujos[0])
        ponto_mais_proximo = pontos_sujos[0]
        for ponto in pontos_sujos:
            if self.bairro.djikstra(self.ponto_atual, ponto) < min_caminho:
                min_caminho = self.bairro.djikstra(self.ponto_atual, ponto)
                ponto_mais_proximo = ponto

        self.ponto_atual = ponto_mais_proximo
        self.tempo_gasto += min_caminho


    def solicitar_carrocinha(self):
        for carrocinha in self.bairro.carrocinhas:
            if carrocinha.disponivel:
                carrocinha.iniciar_rota(self.ponto_atual)
                return

        

            


        
