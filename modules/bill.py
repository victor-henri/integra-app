class Bill:
    def __init__(self,
                 dados_origem,
                 dados_destino,
                 filial_id_origem,
                 filial_id_destino,
                 fornecedores_selecionados,
                 fornecedores_encontrados,
                 fornecedores_pos_insert,
                 comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.filial_id_origem = filial_id_origem
        self.filial_id_destino = filial_id_destino
        self.fornecedores_selecionados = fornecedores_selecionados
        self.fornecedores_encontrados = fornecedores_encontrados
        self.fornecedores_pos_insert = fornecedores_pos_insert
        self.comunicador = comunicador

    def inicia_pagar(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        pagar = iterador.select_pagar(self.fornecedores_selecionados)

        if apagado['apagado'] == 'sim':
            pagar = self.remove_apagado(pagar)

        pagar_tratado = self.trata_pagar(pagar)
        pagar_atualizado = self.atualiza_id_fornecedores(pagar_tratado)
        pagar_log = iterador.insert_pagar(pagar_atualizado)

        return pagar_log

    def trata_pagar(self, pagar):

        for registro in pagar[:]:
            id_filial = int(registro['id_filial'])
            if id_filial != self.filial_id_origem:
                pagar.remove(registro)
            else:
                datas = {'data_emissao': registro['data_emissao'],
                         'data_vencimento': registro['data_vencimento'],
                         'data_pagamento': registro['data_pagamento']}

                datas_tratadas = self.trata_campo_data(datas)

                registro.update({'data_emissao': datas_tratadas['data_emissao']})
                registro.update({'data_vencimento': datas_tratadas['data_vencimento']})
                registro.update({'data_pagamento': datas_tratadas['data_pagamento']})
                registro.update({'id_filial': self.filial_id_destino})
                registro.update({'comunicador': self.comunicador})

        return pagar

    def atualiza_id_fornecedores(self, pagar):

        for registro in pagar:
            atual_id = int(registro['id_fornecedor'])
            novo_id = self.retorna_novoid_fornecedor(atual_id, self.fornecedores_encontrados)
            if novo_id:
                registro.update({'id_fornecedor': novo_id})
            else:
                id_pos_insert = self.retorna_id_pos_insert(atual_id, self.fornecedores_pos_insert)
                registro.update({'id_fornecedor': id_pos_insert})

        return pagar

    @staticmethod
    def remove_apagado(pagar):

        for registro in pagar:
            if registro['apagado'] == 'S':
                pagar.remove(registro)
            else:
                continue

        return pagar

    @staticmethod
    def trata_campo_data(datas):

        for chave, data in datas.items():
            if data is None:
                pass
            elif data == '0000-00-00':
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})

        return datas

    @staticmethod
    def retorna_novoid_fornecedor(atual_id, fornecedores):

        for fornecedor in fornecedores:
            fornecedor_id = int(fornecedor['id_fornecedor'])
            novo_id = int(fornecedor['novo_id'])
            if atual_id == fornecedor_id:
                return novo_id
            else:
                continue

    @staticmethod
    def retorna_id_pos_insert(atual_id, fornecedores):

        for fornecedor in fornecedores:
            fornecedor_id = int(fornecedor['id_fornecedor'])
            fornecedor_id_antigo = int(fornecedor['campo_auxiliar'])
            if atual_id == fornecedor_id_antigo:
                return fornecedor_id
            else:
                continue
