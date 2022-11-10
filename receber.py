from iteradorSQL import IteradorSql


class Receber:
    def __init__(self, dados_origem, dados_destino, filial_id_origem, filial_id_destino,
                 empresas_selecionadas, clientes_selecionados, comunicador):
        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.empresas_selecionadas = empresas_selecionadas
        self.clientes_selecionados = clientes_selecionados
        self.comunicador = comunicador

    def inicia_receber(self, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        receber_origem = iterador.select_receber(self.clientes_selecionados)

        if apagado['apagado'] == 'sim':
            for receber in receber_origem:
                if receber['apagado'] == 'S':
                    receber_origem.remove(receber)
                else:
                    continue

        receber = self.trata_receber(receber_origem)
        receber_log = iterador.insert_receber(receber)

        return receber_log

    def trata_receber(self, receber_origem):
        for receber in receber_origem[:]:
            id_filial = int(receber['id_filial'])

            if id_filial != self.filial_id_origem:
                receber_origem.remove(receber)

            else:
                datas = {'data_venda': receber['data_venda'],
                         'vencimento': receber['vencimento'],
                         'data_baixa': receber['data_baixa'],
                         'data_cadastro': receber['data_cadastro'],
                         'data_alteracao': receber['data_alteracao']}

                datas_tratadas = self.trata_campo_data(datas)

                receber.update({'data_venda': datas_tratadas['data_venda']})
                receber.update({'vencimento': datas_tratadas['vencimento']})
                receber.update({'data_baixa': datas_tratadas['data_baixa']})
                receber.update({'data_cadastro': datas_tratadas['data_cadastro']})
                receber.update({'data_alteracao': datas_tratadas['data_alteracao']})
                receber.update({'id_filial': self.filial_id_destino})
                receber.update({'comunicador': self.comunicador})

        return receber_origem

    @staticmethod
    def trata_campo_data(datas):
        for chave, data in datas.items():
            if data is None:
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})
        return datas
