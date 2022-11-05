from iteradorSQL import IteradorSql


class BarrasAdicional:
    def __init__(self, dados_origem, dados_destino, comunicador, produtos_ids):
        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.produtos_ids = produtos_ids

    def inicia_barras(self, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        barras_origem = iterador.select_barras()

        if apagado['apagado'] == 'sim':
            for barras in barras_origem:
                if barras['apagado'] == 'S':
                    barras_origem.remove(barras)
                else:
                    continue

        barras_selecionados = self.separa_barras_selecionados(barras_origem)
        barras_tratados = self.tratamento_barras(barras_selecionados)
        barras_atualizados = self.atualiza_id_produto(barras_tratados)
        barras_log = iterador.insert_barras(barras_atualizados)

        return barras_log

    def separa_barras_selecionados(self, barras_origem):
        barras_selecionados = []

        for barras in barras_origem:
            id_produto = int(barras['id_produto'])
            if id_produto in self.produtos_ids:
                barras_selecionados.append(barras)
            else:
                continue

        return barras_selecionados

    def tratamento_barras(self, barras_selecionados):
        for barras in barras_selecionados:
            barras['comunicador'] = self.comunicador

        return barras_selecionados

    def atualiza_id_produto(self, barras_selecionados):
        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)

        tabela_produto = {'tabela': 'produto'}
        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)

        for barras in barras_selecionados:
            id_produto_ant = int(barras['id_produto'])

            novo_id = self.busca_id_atual(id_produto_ant, produtos_pos_insert)
            barras.update({'id_produto_ant': id_produto_ant, 'id_produto': novo_id})

        return barras_selecionados

    @staticmethod
    def busca_id_atual(id_produto_ant, produtos):
        for produto in produtos:
            antigo_id = int(produto['campo_auxiliar'])
            novo_id = int(produto['id_produto'])

            if id_produto_ant == antigo_id:
                return novo_id
            else:
                continue
