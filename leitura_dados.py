from Ponto import Ponto

def ler_dados_do_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]  # Remove linhas vazias e espaços extras

        # Validando o número de pontos do grafo pela primeira linha do arquivo
        if len(linhas) < 1:
            raise ValueError("O arquivo está vazio ou não contém o número de pontos.")
        num_pontos = int(linhas[0])
        if num_pontos < 3:
            raise ValueError("O número de pontos deve ser pelo menos 3.")

        # Inicializando o grafo e o lixo acumulado
        adjacencias = {Ponto(i): [] for i in range(num_pontos)}
        lixo_acumulado = {}

        # Lendo as conexões do grafo
        linha_arquivo = 1
        while linha_arquivo < len(linhas) and linhas[linha_arquivo].lower() != "fim":
            try:
                ponto1_id, ponto2_id, custo = map(int, linhas[linha_arquivo].split())
                if ponto1_id < 0 or ponto2_id < 0 or ponto1_id >= num_pontos or ponto2_id >= num_pontos or custo <= 0:
                    raise ValueError(f"Dados inválidos na conexão: {linhas[linha_arquivo]}")
                for ponto in adjacencias.keys():
                    if ponto.id == ponto1_id:
                        ponto1 = ponto
                    if ponto.id == ponto2_id:
                        ponto2 = ponto
                adjacencias[ponto1].append((ponto2, custo))
                adjacencias[ponto2].append((ponto1, custo))
            except ValueError:
                raise ValueError(f"Erro ao processar a conexão: {linhas[linha_arquivo]}")
            linha_arquivo += 1

        # Verificando se a linha "fim" está presente
        if linha_arquivo >= len(linhas) or linhas[linha_arquivo].lower() != "fim":
            raise ValueError("A seção de conexões não termina com 'fim'.")
        linha_arquivo += 1

        # Lendo os pontos do aterro sanitário e centro de zoonoses 
        if linha_arquivo >= len(linhas):
            raise ValueError("Dado do aterro sanitário ausente.")
        aterro_id = int(linhas[linha_arquivo])
        linha_arquivo += 1
        if linha_arquivo >= len(linhas):
            raise ValueError("Dado do centro de zoonoses ausente.")
        zoonoses_id = int(linhas[linha_arquivo])
        for ponto in adjacencias.keys():
            if ponto.id == aterro_id:
                aterro = ponto
            if ponto.id == zoonoses_id:
                zoonoses = ponto
        if aterro_id < 0 or aterro_id >= num_pontos:
            raise ValueError(f"O ponto do aterro sanitário deve estar entre 0 e {num_pontos - 1}.")
        if zoonoses_id < 0 or zoonoses_id >= num_pontos or zoonoses_id == aterro_id:
            raise ValueError(f"O ponto do centro de zoonoses deve estar entre 0 e {num_pontos - 1} e ser diferente do ponto do aterro sanitário.")
        linha_arquivo += 1

        # Lendo o lixo acumulado em cada ponto
        if len(linhas) - linha_arquivo < num_pontos:
            raise ValueError("Dados do lixo acumulado insuficientes.")
        for i in range(num_pontos):
            lixo = float(linhas[linha_arquivo])
            if lixo < 0:
                raise ValueError(f"Quantidade de lixo inválida no ponto {i}: {lixo}")
            lixo_acumulado[i] = lixo
            linha_arquivo += 1
        for ponto in adjacencias.keys():
            ponto.quantidade_de_lixo = lixo_acumulado[ponto.id]

        return adjacencias, aterro, zoonoses

    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return None
    except ValueError as e:
        print(f"Erro nos dados do arquivo: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None