from Ponto import Ponto

def ler_dados_do_arquivo(nome_arquivo):
    try:
        # Abre o arquivo e remove linhas vazias e espaços extras
        with open(nome_arquivo, 'r') as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

        # Validando o número total de pontos do grafo pela primeira linha do arquivo
        if len(linhas) < 1:
            raise ValueError("O arquivo está vazio ou não contém o número de pontos.")
        num_pontos = int(linhas[0])  # Converte o número de pontos para inteiro e armazena-o
        if num_pontos < 3:
            raise ValueError("O número de pontos deve ser pelo menos 3.")

        # Inicializando o grafo e o lixo acumulado
        adjacencias = {Ponto(i): [] for i in range(num_pontos)}
        lixo_acumulado = {}

        # Lendo as conexões do grafo
        linha_arquivo = 1  # Começa a leitura na segunda linha
        while linha_arquivo < len(linhas) and linhas[linha_arquivo].lower() != "fim":
            try:
                # Cada linha deve conter dois IDs de pontos e o custo da conexão entre eles
                ponto1_id, ponto2_id, custo = map(int, linhas[linha_arquivo].split())
                # Verifica se os IDs e o custo são válidos
                if ponto1_id < 0 or ponto2_id < 0 or ponto1_id >= num_pontos or ponto2_id >= num_pontos or custo <= 0:
                    raise ValueError(f"Dados inválidos na conexão: {linhas[linha_arquivo]}")
                # Busca os objetos Ponto correspondentes aos IDs fornecidos
                for ponto in adjacencias.keys():
                    if ponto.id == ponto1_id:
                        ponto1 = ponto
                    if ponto.id == ponto2_id:
                        ponto2 = ponto
                # Adiciona a conexão ao grafo (nos dois sentidos, pois o grafo é não direcionado)
                adjacencias[ponto1].append((ponto2, custo))
                adjacencias[ponto2].append((ponto1, custo))
            except ValueError:
                # Levanta um erro em caso de problemas no processamento da conexão
                raise ValueError(f"Erro ao processar a conexão: {linhas[linha_arquivo]}")
            linha_arquivo += 1  # Avança para a próxima linha

        # Verificando se a linha "fim", que finaliza a seção de conexões, está presente
        if linha_arquivo >= len(linhas) or linhas[linha_arquivo].lower() != "fim":
            raise ValueError("A seção de conexões não termina com 'fim'.")
        linha_arquivo += 1  # Avança para a linha seguinte

        # Lendo os IDs do aterro sanitário e do centro de zoonoses
        if linha_arquivo >= len(linhas):
            raise ValueError("Dado do aterro sanitário ausente.")
        aterro_id = int(linhas[linha_arquivo])  # Lê o ID do aterro sanitário
        linha_arquivo += 1
        if linha_arquivo >= len(linhas):
            raise ValueError("Dado do centro de zoonoses ausente.")
        zoonoses_id = int(linhas[linha_arquivo])  # Lê o ID do centro de zoonoses
        # Busca os objetos Ponto correspondentes aos IDs fornecidos
        for ponto in adjacencias.keys():
            if ponto.id == aterro_id:
                aterro = ponto
            if ponto.id == zoonoses_id:
                zoonoses = ponto
        # Valida os IDs do aterro sanitário e centro de zoonoses
        if aterro_id < 0 or aterro_id >= num_pontos:
            raise ValueError(f"O ponto do aterro sanitário deve estar entre 0 e {num_pontos - 1}.")
        if zoonoses_id < 0 or zoonoses_id >= num_pontos or zoonoses_id == aterro_id:
            raise ValueError(f"O ponto do centro de zoonoses deve estar entre 0 e {num_pontos - 1} e ser diferente do ponto do aterro sanitário.")
        linha_arquivo += 1  # Avança para a próxima linha

        # Lendo o lixo acumulado em cada ponto
        # Cada linha deve conter a quantidade de lixo acumulado em um ponto, indo do primeiro ao último, de acordo com o ID do ponto
        if len(linhas) - linha_arquivo < num_pontos:
            raise ValueError("Dados do lixo acumulado insuficientes.")
        for i in range(num_pontos):
            lixo = float(linhas[linha_arquivo])  # Converte a quantidade de lixo para float e armazena-o
            if lixo < 0:
                raise ValueError(f"Quantidade de lixo inválida no ponto {i}: {lixo}")
            lixo_acumulado[i] = lixo  # Armazena a quantidade de lixo do ponto i
            linha_arquivo += 1  # Avança para a próxima linha
        # Atualiza o atributo 'quantidade_de_lixo' de cada ponto
        for ponto in adjacencias.keys():
            ponto.quantidade_de_lixo = lixo_acumulado[ponto.id]

        # Retorna os dados lidos: o grafo, o aterro sanitário e o centro de zoonoses
        return adjacencias, aterro, zoonoses

    except FileNotFoundError:
        # Trata o erro de arquivo não encontrado
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return None
    except ValueError as e:
        # Trata erros de validação específicos dos dados do arquivo
        print(f"Erro nos dados do arquivo: {e}")
        return None
    except Exception as e:
        # Trata erros inesperados
        print(f"Erro inesperado: {e}")
        return None