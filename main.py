from copy import deepcopy
from leitura_dados import ler_dados_do_arquivo
from Grafo import Grafo
from Ponto import Ponto
from Caminhao import Caminhao
from Carrocinha import Carrocinha

# Caminho do arquivo de entrada
arquivo_entrada = "entrada.txt"

# Lendo os dados do arquivo
adjacencias, aterro, zoonoses = ler_dados_do_arquivo(arquivo_entrada)
bairro_original = Grafo(adjacencias, aterro, zoonoses)


try:
    sucesso = False
    # a quantidade de caminhões começará em 1 e aumentará a cada teste falho, até que seja
    # possível coletar todo o lixo do bairro em no máximo 8 horas
    quantidade_de_caminhoes = 1
    while True:
        # começaremos com 3 funcionários por caminhão, e aumentaremos até 5 até que seja possível realizar
        # a coleta em no máximo 8 horas
        for funcionarios_por_caminhao in range(3, 6):
            # dados os parâmetros de caminhões e funcionários, simularemos a coleta e calcularemos o tempo gasto
            # para conclusão

            bairro = deepcopy(bairro_original)

            for ponto in bairro.adjacencias.keys():
                print("ponto", ponto.id)
                print(ponto.quantidade_de_cachorros)
                print(ponto.quantidade_de_gatos)
                print(ponto.quantidade_de_ratos)
                print("lixo", ponto.quantidade_de_lixo)
                print("=====================")

            carrocinhaScoobyDoo = Carrocinha(bairro)
            carrocinhaBolt = Carrocinha(bairro)
            carrocinhaBidu = Carrocinha(bairro)
            bairro.carrocinhas = [carrocinhaScoobyDoo, carrocinhaBolt, carrocinhaBidu]

            for i in range(quantidade_de_caminhoes):
                caminhao = Caminhao(bairro, funcionarios_por_caminhao)
                bairro.caminhoes.append(caminhao)

            TEMPO_MAXIMO = 8*60 # consideramos nossa unidade de tempo em minutos

            tempo_esgotado = False
            while bairro.tem_pontos_sujos() and not tempo_esgotado:
                for caminhao in bairro.caminhoes:
                    caminhao.sessao_de_coleta()
                    if caminhao.tempo_gasto > TEMPO_MAXIMO:
                        tempo_esgotado = True

                for carrocinha in bairro.carrocinhas:
                    carrocinha.disponivel = True
                    if carrocinha.tempo_gasto > TEMPO_MAXIMO:
                        tempo_esgotado = True

            if not tempo_esgotado:
                sucesso = True
                break
        if sucesso:
            break

        quantidade_de_caminhoes += 1
except Exception:
    pass

print(f"""
Os valores mínimos para realizar a coleta de lixo em 8 horas são:
Caminhões - {quantidade_de_caminhoes}
Funcionários por caminhão - {funcionarios_por_caminhao}
""")