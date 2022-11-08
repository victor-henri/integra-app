from iteradorSQL import IteradorSql


class PrecoFilial:
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

        precos_origem = iterador.select_preco_filial()

        if apagado['apagado'] == 'sim':
            for precos in precos_origem:
                if precos['apagado'] == 'S':
                    precos_origem.remove(precos)
                else:
                    continue

        precos_filial_selecionados = self.separa_precos_selecionados(precos_origem)
        precos_filial_tratados = self.tratamento_precos_filial(precos_filial_selecionados)
        precos_filial_atualizados = self.atualiza_id_produto(precos_filial_tratados)
        preco_filial_log = iterador.insert_precos_filial(precos_filial_atualizados)

        return preco_filial_log

    def separa_precos_selecionados(self, precos_origem):
        precos_selecionados = []

        for preco in precos_origem:
            produto_id = int(preco['id_produto'])
            preco_filial = int(preco['id_filial'])
            if produto_id in self.produtos_ids and preco_filial == self.filial_id_origem:
                precos_selecionados.append(preco)
            else:
                continue

        return precos_selecionados

    def tratamento_precos_filial(self, precos_filial_selecionados):
        for preco in precos_filial_selecionados:

            datas = {'inicio': preco['inicio_promocao'],
                     'final': preco['final_promocao']}

            datas_tratadas = self.trata_campo_data(datas)

            preco.update({'inicio_promocao': datas_tratadas['inicio']})
            preco.update({'final_promocao': datas_tratadas['final']})
            preco.update({'id_filial': self.filial_id_destino})
            preco.update({'comunicador': self.comunicador})

        return precos_filial_selecionados

    def atualiza_id_produto(self, precos):
        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)

        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for preco in precos:
            id_produto_ant = int(preco['id_produto'])

            novo_id = self.busca_id_atual(id_produto_ant, produtos_pos_insert)
            preco.update({'id_produto_ant': id_produto_ant, 'id_produto': novo_id})

        return precos

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
