class Supplier():
    def __init__(self, dados_origem, dados_destino, fornecedores_selecionados, comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.fornecedores_selecionados = fornecedores_selecionados
        self.comunicador = comunicador
        self.fornecedores_pos_insert = None
        self.fornecedores_encontrados_tratados = None
        self.fornecedores_nencontrados_tratados = None

    def inicia_fornecedores(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        fornecedores_origem = iterador.select_fornecedor_origem(self.fornecedores_selecionados)
        fornecedores_destino = iterador.select_fornecedor_destino()

        if apagado['apagado'] == 'sim':
            fornecedores_origem = self.remove_apagado(fornecedores_origem)

        fornecedores = self.procura_fornecedores(fornecedores_origem, fornecedores_destino)
        self.fornecedores_encontrados_tratados = self.trata_fornecedores(fornecedores['fornecedores_encontrados'])
        self.fornecedores_nencontrados_tratados = self.trata_fornecedores(fornecedores['fornecedores_nencontrados'])

        fornecedores_log = iterador.insert_fornecedor(self.fornecedores_nencontrados_tratados)
        self.fornecedores_pos_insert = iterador.consulta_fornecedor_pos_insert()

        return fornecedores_log

    def procura_fornecedores(self, fornecedores_origem, fornecedores_destino):

        fornecedores_encontrados = []
        fornecedores_nencontrados = []

        for fornecedor in fornecedores_origem:
            cnpj = fornecedor['cnpj']
            novo_id = self.retorna_fornecedor(cnpj, fornecedores_destino)
            if novo_id:
                fornecedor.update({'novo_id': novo_id})
                fornecedores_encontrados.append(fornecedor)
            else:
                fornecedor.update({'novo_id': None})
                fornecedores_nencontrados.append(fornecedor)

        return {'fornecedores_encontrados': fornecedores_encontrados,
                'fornecedores_nencontrados': fornecedores_nencontrados}

    def trata_fornecedores(self, fornecedores):

        for fornecedor in fornecedores:
            fornecedor.update({'comunicador': self.comunicador})

        return fornecedores

    @staticmethod
    def remove_apagado(fornecedores):

        for registro in fornecedores:
            if registro['apagado'] == 'S':
                fornecedores.remove(registro)
            else:
                continue

        return fornecedores

    @staticmethod
    def retorna_fornecedor(cnpj_origem, fornecedores):

        for fornecedor in fornecedores:
            cnpj_destino = fornecedor['cnpj']
            fornecedor_id = int(fornecedor['id_fornecedor'])
            if cnpj_origem == cnpj_destino:
                return fornecedor_id
            else:
                continue

    def retorna_fornecedores_tratados(self):
        return self.fornecedores_encontrados_tratados

    def retorna_fornecedores_pos_insert(self):
        return self.fornecedores_pos_insert
