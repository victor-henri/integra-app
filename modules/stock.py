class Stock:
    def __init__(self, dados_origem, dados_destino, comunicador, filial_id_origem, filial_id_destino, produtos_ids):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.produtos_ids = produtos_ids

    def inicia_estoque(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        estoque = iterador.select_estoque()

        if apagado['apagado'] == 'sim':
            estoque = self.remove_apagado(estoque)

        id_produtos = self.produtos_ids['id_produtos']
        produtos_encontrados = self.produtos_ids['produtos_encontrados']

        estoque_selecionados = self.separa_selecionados(id_produtos, estoque)
        estoque_tratado = self.tratamento_estoque(produtos_encontrados, estoque_selecionados)
        estoque_log = iterador.insert_estoque(estoque_tratado)

        return estoque_log

    @staticmethod
    def remove_apagado(estoque):

        for registro in estoque:
            if registro['apagado'] == 'S':
                estoque.remove(registro)
            else:
                continue

        return estoque

    def separa_selecionados(self, id_produtos, estoque):

        estoque_selecionados = []

        for registro in estoque:
            produto_id = int(registro['id_produto'])
            estoque_filial_id = int(registro['id_filial'])

            if produto_id in id_produtos and estoque_filial_id == self.filial_id_origem:
                estoque_selecionados.append(registro)
            else:
                continue

        return estoque_selecionados

    def tratamento_estoque(self, produtos_encontrados, estoque):

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for registro in estoque:
            antigo_id = int(registro['id_produto'])
            id_encontrado = self.compara_produto(antigo_id, produtos_encontrados)
            if id_encontrado is None:
                novo_produto_id = self.procura_id_produto(antigo_id, produtos_pos_insert)
                registro.update({'id_produto_ant': registro['id_produto']})
                registro.update({'id_produto': novo_produto_id})
                registro.update({'existe': 'N'})
            else:
                registro.update({'id_produto_ant': registro['id_produto']})
                registro.update({'id_produto': id_encontrado})
                registro.update({'existe': 'S'})

            datas = {'data_cadastro': registro['data_cadastro'],
                     'data_alteracao': registro['data_alteracao']}

            datas_tratadas = self.trata_campo_data(datas)

            registro.update({'data_cadastro': datas_tratadas['data_cadastro']})
            registro.update({'data_alteracao': datas_tratadas['data_alteracao']})
            registro.update({'id_filial': self.filial_id_destino})
            registro.update({'comunicador': self.comunicador})

        return estoque

    @staticmethod
    def compara_produto(antigo_id, produtos):

        for produto in produtos:
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
