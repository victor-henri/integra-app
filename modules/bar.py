class Bar:

    def __init__(self, dados_origem, dados_destino, comunicador, produtos_ids):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.produtos_ids = produtos_ids

    def inicia_barras(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        barras = iterador.select_barras()

        if apagado['apagado'] == 'sim':
            barras = self.remove_apagado(barras)

        id_produtos = self.produtos_ids['id_produtos']
        produtos_encontrados = self.produtos_ids['produtos_encontrados']

        barras_selecionados = self.separa_barras_selecionados(id_produtos, barras)
        barras_tratados = self.tratamento_barras(produtos_encontrados, barras_selecionados)
        barras_log = iterador.insert_barras(barras_tratados)

        return barras_log

    @staticmethod
    def remove_apagado(barras):

        for registro in barras:
            if registro['apagado'] == 'S':
                barras.remove(registro)
            else:
                continue

        return barras

    @staticmethod
    def separa_barras_selecionados(id_produtos, barras):

        barras_selecionados = []

        for registro in barras:
            id_produto = int(registro['id_produto'])
            if id_produto in id_produtos:
                barras_selecionados.append(registro)
            else:
                continue

        return barras_selecionados

    def tratamento_barras(self, produtos_encontrados, barras):

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for registro in barras:
            antigo_id = int(registro['id_produto'])
            id_encontrado = self.compara_produto(antigo_id, produtos_encontrados)
            if id_encontrado is None:
                novo_id = self.busca_id_atual(antigo_id, produtos_pos_insert)
                registro.update({'id_produto_ant': antigo_id})
                registro.update({'id_produto': novo_id})
            else:
                registro.update({'id_produto_ant': registro['id_produto']})
                registro.update({'id_produto': id_encontrado})

            registro['comunicador'] = self.comunicador

        return barras

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
