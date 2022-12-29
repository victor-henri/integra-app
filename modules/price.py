class Price:
    def __init__(self, dados_origem, dados_destino, comunicador, filial_id_origem, filial_id_destino, produtos_ids):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.produtos_ids = produtos_ids

    def inicia_precos_filial(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        precos = iterador.select_preco_filial()

        if apagado['apagado'] == 'sim':
            precos = self.remove_apagado(precos)

        id_produtos = self.produtos_ids['id_produtos']
        produtos_encontrados = self.produtos_ids['produtos_encontrados']

        precos_filial_selecionados = self.separa_precos_selecionados(id_produtos, precos)
        precos_filial_tratados = self.tratamento_precos_filial(produtos_encontrados, precos_filial_selecionados)
        preco_filial_log = iterador.insert_precos_filial(precos_filial_tratados)

        return preco_filial_log

    @staticmethod
    def remove_apagado(precos):

        for registro in precos:
            if registro['apagado'] == 'S':
                precos.remove(registro)
            else:
                continue

        return precos

    def separa_precos_selecionados(self, id_produtos, precos):

        precos_selecionados = []

        for registro in precos:
            produto_id = int(registro['id_produto'])
            preco_filial = int(registro['id_filial'])
            if produto_id in id_produtos and preco_filial == self.filial_id_origem:
                precos_selecionados.append(registro)
            else:
                continue

        return precos_selecionados

    def tratamento_precos_filial(self, produtos_encontrados, precos):

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for preco in precos[:]:
            antigo_id = int(preco['id_produto'])
            id_encontrado = self.compara_produto(antigo_id, produtos_encontrados)
            if id_encontrado is None:
                novo_id = self.busca_id_atual(antigo_id, produtos_pos_insert)
                preco.update({'id_produto_ant': antigo_id})
                preco.update({'id_produto': novo_id})
            else:
                precos.remove(preco)

            datas = {'inicio': preco['inicio_promocao'],
                     'final': preco['final_promocao']}

            datas_tratadas = self.trata_campo_data(datas)

            preco.update({'inicio_promocao': datas_tratadas['inicio']})
            preco.update({'final_promocao': datas_tratadas['final']})
            preco.update({'id_filial': self.filial_id_destino})
            preco.update({'comunicador': self.comunicador})

        return precos

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
    def busca_id_atual(id_produto_ant, produtos):

        for produto in produtos:
            antigo_id = int(produto['campo_auxiliar'])
            novo_id = int(produto['id_produto'])
            if id_produto_ant == antigo_id:
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
