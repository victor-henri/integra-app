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

        lotes_origem = iterador.select_lote()

        if apagado['apagado'] == 'sim':
            for lote in lotes_origem:
                if lote['apagado'] == 'S':
                    lotes_origem.remove(lote)
                else:
                    continue

        lotes_selecionados = self.separa_lotes_selecionados(lotes_origem)
        lotes = self.tratamento_lote(lotes_selecionados)
        lotes_log = iterador.insert_lote(lotes)

        return lotes_log

    def separa_lotes_selecionados(self, lotes_origem):
        lotes_selecionados = []

        for lote in lotes_origem:
            id_produto = int(lote['id_produto'])
            lote_filial = int(lote['id_filial'])
            if id_produto in self.produtos_ids and lote_filial == self.filial_id_origem:
                lotes_selecionados.append(lote)
            else:
                continue

        return lotes_selecionados

    def tratamento_lote(self, lotes_selecionados):
        for lote in lotes_selecionados:

            datas = {'validade': lote['data_validade'], 'fabricacao': lote['data_fabricacao']}

            datas_tratadas = self.trata_campo_data(datas)

            lote.update({'data_validade': datas_tratadas['validade']})
            lote.update({'data_fabricacao': datas_tratadas['fabricacao']})
            lote.update({'comunicador': self.comunicador})
            lote.update({'id_filial': self.filial_id_destino})

        return lotes_selecionados

    @staticmethod
    def trata_campo_data(datas):
        for chave, data in datas.items():
            if data is None:
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})
        return datas
