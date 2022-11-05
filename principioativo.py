from iteradorSQL import IteradorSql


class PrincipioAtivo:
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
            for principio in principios_origem:
                if principio['apagado'] == 'S':
                    principios_origem.remove(principio)
                else:
                    continue

        principios = self.procura_principios(principios_origem, principios_destino)
        self.principios_encontrados_tratados = self.tratamento_principios(principios['principios_encontrados'])
        self.principios_nencontrados_tratados = self.tratamento_principios(principios['principios_nencontrados'])
        principio_ativo_log = iterador.insert_principios(self.principios_nencontrados_tratados)

        return principio_ativo_log

    def procura_principios(self, principios_origem, principios_destino):
        principios_encontrados = []
        principios_nencontrados = []

        for principio in principios_origem:
            descricao = principio['descricao']
            novo_id = self.retorna_principio_ativo(descricao_origem=descricao,
                                                   principios_destino=principios_destino)
            if novo_id:
                principio.update({'novo_id': novo_id, 'existe': 1})
                principios_encontrados.append(principio)
            else:
                principio.update({'novo_id': None, 'existe': 0})
                principios_nencontrados.append(principio)

        return {'principios_encontrados': principios_encontrados,
                'principios_nencontrados': principios_nencontrados}

    @staticmethod
    def retorna_principio_ativo(descricao_origem, principios_destino):
        for principio in principios_destino:
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
        principios_encontrados_tratados = self.principios_encontrados_tratados
        return principios_encontrados_tratados
