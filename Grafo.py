import heapq
from random import randint

class Grafo:
    def __init__(self, adjacencias, aterro, zoonoses):
        self.adjacencias = adjacencias
        self.aterro = aterro
        self.zoonoses = zoonoses
        self.carrocinhas = []
        self.caminhoes = []
        

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.adjacencias:
            self.adjacencias[origem] = []
        if destino not in self.adjacencias:
            self.adjacencias[destino] = []
        self.adjacencias[origem].append((destino, peso))
        self.adjacencias[destino].append((origem, peso))


    def dijkstra(self, origem, destino):
        distancias = {vertice: float('inf') for vertice in self.adjacencias}
        anteriores = {vertice: None for vertice in self.adjacencias}  # Para reconstruir o caminho
        distancias[origem] = 0
        heap = [(0, origem)]  # (distância acumulada, vértice atual)

        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            if vertice_atual == destino:
                break

            if dist_atual > distancias[vertice_atual]:
                continue

            for vizinho, peso in self.adjacencias[vertice_atual]:
                nova_dist = dist_atual + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(heap, (nova_dist, vizinho))


        caminho = self.reconstruir_caminho(anteriores, destino)
        return distancias[destino], caminho


    def reconstruir_caminho(self, anteriores, destino):
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        return caminho[::-1]  # Inverter para ficar na ordem correta
    

    def tem_pontos_sujos(self):
        for ponto in self.adjacencias.keys():
            if ponto.quantidade_de_lixo > 0:
                return True
        return False
    
    
    def movimentar_animais(self):
        movimentacoes = {ponto: {'quantidade_de_ratos':0, 'quantidade_de_gatos':0, 'quantidade_de_cachorros':0} for ponto in self.adjacencias}
        for ponto in self.adjacencias:
            if ponto.quantidade_de_gatos > 0:
                if ponto.quantidade_de_ratos > 0:
                    ponto_proximo = self.adjacencias[ponto][randint(0, len(self.adjacencias[ponto])-1)]
                    movimentacoes[ponto_proximo]['quantidade_de_ratos'] += ponto.quantidade_de_ratos-1
                    ponto.quantidade_de_ratos = 0
                if ponto.quantidade_de_cachorros > 0:
                    ponto_proximo = self.adjacencias[ponto][randint(0, len(self.adjacencias[ponto])-1)]
                    movimentacoes[ponto_proximo]['quantidade_de_gatos'] += ponto.quantidade_de_gatos
                    ponto.quantidade_de_gatos = 0
            if ponto.quantidade_de_lixo == 0:
                ponto_proximo = self.adjacencias[ponto][randint(0, len(self.adjacencias[ponto])-1)]
                movimentacoes[ponto_proximo]['quantidade_de_ratos'] += ponto.quantidade_de_ratos
                ponto.quantidade_de_ratos = 0
                ponto_proximo = self.adjacencias[ponto][randint(0, len(self.adjacencias[ponto])-1)]
                movimentacoes[ponto_proximo]['quantidade_de_gatos'] += ponto.quantidade_de_gatos
                ponto.quantidade_de_gatos = 0
                ponto_proximo = self.adjacencias[ponto][randint(0, len(self.adjacencias[ponto])-1)]
                movimentacoes[ponto_proximo]['quantidade_de_cachorros'] += ponto.quantidade_de_cachorros
                ponto.quantidade_de_cachorros = 0
        for ponto in self.adjacencias:
            ponto.quantidade_de_ratos += movimentacoes[ponto]['quantidade_de_ratos']
            ponto.quantidade_de_gatos += movimentacoes[ponto]['quantidade_de_gatos']
            ponto.quantidade_de_cachorros += movimentacoes[ponto]['quantidade_de_cachorros']