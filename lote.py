from iteradorSQL import IteradorSql


class Lote:
    def __init__(self, dados_origem, dados_destino, comunicador, filial_id_origem, filial_id_destino, produtos_ids):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.produtos_ids = produtos_ids

    def inicia_lotes(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        lote = iterador.select_lote()

        if apagado['apagado'] == 'sim':
            lote = self.remove_apagado(lote)

        id_produtos = self.produtos_ids['id_produtos']
        produtos_encontrados = self.produtos_ids['produtos_encontrados']

        lotes_selecionados = self.separa_lotes_selecionados(id_produtos, lote)
        lotes_tratados = self.tratamento_lote(produtos_encontrados, lotes_selecionados)
        lotes_log = iterador.insert_lote(lotes_tratados)

        return lotes_log

    @staticmethod
    def remove_apagado(lote):

        for registro in lote:
            if registro['apagado'] == 'S':
                lote.remove(registro)
            else:
                continue

        return lote

    def separa_lotes_selecionados(self, id_produtos, lote):

        lotes_selecionados = []

        for registro in lote:
            id_produto = int(registro['id_produto'])
            lote_filial = int(registro['id_filial'])
            if id_produto in id_produtos and lote_filial == self.filial_id_origem:
                lotes_selecionados.append(registro)
            else:
                continue

        return lotes_selecionados

    def tratamento_lote(self, produtos_encontrados, lotes):

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for lote in lotes:
            antigo_id = int(lote['id_produto'])
            id_encontrado = self.compara_produto(antigo_id, produtos_encontrados)
            if id_encontrado is None:
                novo_id = self.busca_id_atual(antigo_id, produtos_pos_insert)
                lote.update({'id_produto_ant': antigo_id})
                lote.update({'id_produto': novo_id})
            else:
                lote.update({'id_produto_ant': lote['id_produto']})
                lote.update({'id_produto': id_encontrado})

            datas = {'validade': lote['data_validade'], 'fabricacao': lote['data_fabricacao']}

            datas_tratadas = self.trata_campo_data(datas)

            lote.update({'data_validade': datas_tratadas['validade']})
            lote.update({'data_fabricacao': datas_tratadas['fabricacao']})
            lote.update({'id_filial': self.filial_id_destino})
            lote.update({'comunicador': self.comunicador})

        return lotes

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
