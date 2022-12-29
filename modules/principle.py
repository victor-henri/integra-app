class Principle:
    def __init__(self, dados_origem, dados_destino, comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.principios_encontrados_tratados = None
        self.principios_nencontrados_tratados = None

    def inicia_principios_ativos(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        principios_origem = iterador.select_principio_ativo_origem()
        principios_destino = iterador.select_principio_ativo_destino()

        if apagado['apagado'] == 'sim':
            principios_origem = self.remove_apagado(principios_origem)

        principios = self.procura_principios(principios_origem, principios_destino)
        self.principios_encontrados_tratados = self.tratamento_principios(principios['principios_encontrados'])
        self.principios_nencontrados_tratados = self.tratamento_principios(principios['principios_nencontrados'])
        principio_ativo_log = iterador.insert_principios(self.principios_nencontrados_tratados)

        return principio_ativo_log

    @staticmethod
    def remove_apagado(principios):

        for registro in principios:
            if registro['apagado'] == 'S':
                principios.remove(registro)
            else:
                continue

        return principios

    def procura_principios(self, principios_origem, principios_destino):

        principios_encontrados = []
        principios_nencontrados = []

        for principio in principios_origem:
            descricao = principio['descricao']
            novo_id = self.retorna_principio_ativo(descricao, principios_destino)
            if novo_id:
                principio.update({'novo_id': novo_id, 'existe': 1})
                principios_encontrados.append(principio)
            else:
                principio.update({'novo_id': None, 'existe': 0})
                principios_nencontrados.append(principio)

        return {'principios_encontrados': principios_encontrados,
                'principios_nencontrados': principios_nencontrados}

    @staticmethod
    def retorna_principio_ativo(descricao_origem, principios):

        for principio in principios:
            descricao_destino = principio['descricao']
            principio_id = int(principio['id_principio_ativo'])
            if descricao_origem == descricao_destino:
                return principio_id
            else:
                continue

    def tratamento_principios(self, principios):

        for principio in principios:
            principio.update({'comunicador': self.comunicador})

        return principios

    def retorna_principios_tratados(self):
        return self.principios_encontrados_tratados
