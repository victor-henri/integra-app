from iteradorSQL import IteradorSql


class EstoqueMinimo:
    def __init__(self, dados_origem, dados_destino, comunicador, filial_id_origem, filial_id_destino, produtos_ids):
        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.produtos_ids = produtos_ids

    def inicia_estoque_minimo(self, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        estoque_minimo_origem = iterador.select_estoque()

        if apagado['apagado'] == 'sim':
            for estoque in estoque_minimo_origem:
                if estoque['apagado'] == 'S':
                    estoque_minimo_origem.remove(estoque)
                else:
                    continue

        id_produtos = self.produtos_ids['id_produtos']
        produtos_encontrados = self.produtos_ids['produtos_encontrados']

        estoque_minimo_selecionados = self.separa_estmin_selecionados(id_produtos, estoque_minimo_origem)
        estoque_minimo_tratado = self.tratamento_estoque_minimo(produtos_encontrados, estoque_minimo_selecionados)
        estoque_minimo_log = iterador.insert_estoque(estoque_minimo_tratado)

        return estoque_minimo_log

    def separa_estmin_selecionados(self, id_produtos, estoque_minimo_origem):
        estmin_selecionados = []

        for estoque in estoque_minimo_origem:
            produto_id = int(estoque['id_produto'])
            estoque_filial_id = int(estoque['id_filial'])

            if produto_id in id_produtos and estoque_filial_id == self.filial_id_origem:
                estmin_selecionados.append(estoque)
            else:
                continue

        return estmin_selecionados

    def tratamento_estoque_minimo(self, produtos_encontrados, estoque_minimo_selecionados):
        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for estoque in estoque_minimo_selecionados:
            antigo_id = int(estoque['id_produto'])
            id_encontrado = self.compara_produto(antigo_id, produtos_encontrados)

            if id_encontrado is None:
                novo_produto_id = self.procura_id_produto(antigo_id, produtos_pos_insert)
                estoque.update({'id_produto_ant': estoque['id_produto']})
                estoque.update({'id_produto': novo_produto_id})
                estoque.update({'existe': 'N'})
            else:
                estoque.update({'id_produto_ant': estoque['id_produto']})
                estoque.update({'id_produto': id_encontrado})
                estoque.update({'existe': 'S'})

            datas = {'data_cadastro': estoque['data_cadastro'],
                     'data_alteracao': estoque['data_alteracao']}

            datas_tratadas = self.trata_campo_data(datas)

            estoque.update({'data_cadastro': datas_tratadas['data_cadastro']})
            estoque.update({'data_alteracao': datas_tratadas['data_alteracao']})
            estoque.update({'id_filial': self.filial_id_destino})
            estoque.update({'comunicador': self.comunicador})

        return estoque_minimo_selecionados

    @staticmethod
    def compara_produto(antigo_id, produtos_encontrados):
        for produto in produtos_encontrados:
            id_produto = int(produto['id_produto'])
            novo_id = int(produto['novo_id'])

            if antigo_id == id_produto:
                return novo_id
            else:
                continue

    @staticmethod
    def trata_campo_data(datas):
        for chave, data in datas.items():
            if data is None:
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})
        return datas

    @staticmethod
    def procura_id_produto(produto_id_antigo, produtos):
        for produto in produtos:
            if produto['campo_auxiliar'] is None:
                pass
            else:
                produto_id_antigo_armazenado = int(produto['campo_auxiliar'])
                novo_produto_id = int(produto['id_produto'])
                if produto_id_antigo == produto_id_antigo_armazenado:
                    return novo_produto_id
                else:
                    continue
