from iteradorSQL import IteradorSql


class Receber:
    def __init__(self,
                 dados_origem,
                 dados_destino,
                 filial_id_origem,
                 filial_id_destino,
                 empresas_selecionadas,
                 clientes_selecionados,
                 comunicador):

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
        receber = iterador.select_receber(self.clientes_selecionados)

        if apagado['apagado'] == 'sim':
            receber = self.remove_apagado(receber)

        receber_tratado = self.trata_receber(receber)
        receber_log = iterador.insert_receber(receber_tratado)

        return receber_log

    def trata_receber(self, receber):

        for registro in receber[:]:
            id_filial = int(registro['id_filial'])
            if id_filial != self.filial_id_origem:
                receber.remove(registro)
            else:
                datas = {'data_venda': registro['data_venda'],
                         'vencimento': registro['vencimento'],
                         'data_baixa': registro['data_baixa'],
                         'data_cadastro': registro['data_cadastro'],
                         'data_alteracao': registro['data_alteracao']}

                datas_tratadas = self.trata_campo_data(datas)

                registro.update({'data_venda': datas_tratadas['data_venda']})
                registro.update({'vencimento': datas_tratadas['vencimento']})
                registro.update({'data_baixa': datas_tratadas['data_baixa']})
                registro.update({'data_cadastro': datas_tratadas['data_cadastro']})
                registro.update({'data_alteracao': datas_tratadas['data_alteracao']})
                registro.update({'id_filial': self.filial_id_destino})
                registro.update({'comunicador': self.comunicador})

        return receber

    @staticmethod
    def remove_apagado(receber):

        for registro in receber:
            if registro['apagado'] == 'S':
                receber.remove(registro)
            else:
                continue

        return receber

    @staticmethod
    def trata_campo_data(datas):

        for chave, data in datas.items():
            if data is None:
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})

        return datas
