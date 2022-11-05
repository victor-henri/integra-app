from iteradorSQL import IteradorSql


class Pagar:
    def __init__(self, dados_origem, dados_destino, filial_id_destino,
                 fornecedores_selecionados, fornecedores_encontrados, fornecedores_pos_insert, comunicador):
        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.filial_id_destino = filial_id_destino
        self.fornecedores_selecionados = fornecedores_selecionados
        self.fornecedores_encontrados = fornecedores_encontrados
        self.fornecedores_pos_insert = fornecedores_pos_insert
        self.comunicador = comunicador

    def inicia_pagar(self, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        pagar_origem = iterador.select_pagar(self.fornecedores_selecionados)

        if apagado['apagado'] == 'sim':
            for pagar in pagar_origem:
                if pagar['apagado'] == 'S':
                    pagar_origem.remove(pagar)
                else:
                    continue

        # pagar_nao_baixado = self.remove_pagar_baixado(pagar_origem)
        pagar_tratado = self.trata_pagar(pagar_origem)
        pagar = self.atualiza_id_fornecedores(pagar_tratado)
        pagar_log = iterador.insert_pagar(pagar)

        return pagar_log

    def remove_pagar_baixado(self, pagar_origem):
        pagars_nao_baixados = []
        for pagar in pagar_origem:
            if pagar['dt_pgto'] is None:
                pagars_nao_baixados.append(pagar)
                continue
            else:
                continue
        return pagars_nao_baixados

    def trata_pagar(self, pagar_origem):
        for pagar in pagar_origem:

            datas = {'data_emissao': pagar['data_emissao'],
                     'data_vencimento': pagar['data_vencimento'],
                     'data_pagamento': pagar['data_pagamento']}

            datas_tratadas = self.trata_campo_data(datas)

            pagar.update({'data_emissao': datas_tratadas['data_emissao']})
            pagar.update({'data_vencimento': datas_tratadas['data_vencimento']})
            pagar.update({'data_pagamento': datas_tratadas['data_pagamento']})
            pagar.update({'id_filial': self.filial_id_destino})
            pagar.update({'comunicador': self.comunicador})

        return pagar_origem

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

    def atualiza_id_fornecedores(self, pagar_tratado):
        for pagar in pagar_tratado:

            atual_id = int(pagar['id_fornecedor'])
            novo_id = self.retorna_novoid_fornecedor(atual_id)

            if novo_id:
                pagar.update({'id_fornecedor': novo_id})
            else:
                id_pos_insert = self.retorna_id_pos_insert(atual_id)
                pagar.update({'id_fornecedor': id_pos_insert})

        return pagar_tratado

    def retorna_novoid_fornecedor(self, atual_id):
        for fornecedor in self.fornecedores_encontrados:
            fornecedor_id = int(fornecedor['id_fornecedor'])
            novo_id = int(fornecedor['novo_id'])

            if atual_id == fornecedor_id:
                return novo_id
            else:
                continue

    def retorna_id_pos_insert(self, atual_id):
        for fornecedor in self.fornecedores_pos_insert:
            fornecedor_id = int(fornecedor['id_fornecedor'])
            fornecedor_id_antigo = int(fornecedor['campo_auxiliar'])

            if atual_id == fornecedor_id_antigo:
                return fornecedor_id
            else:
                continue
