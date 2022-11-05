from iteradorSQL import IteradorSql


class Fabricante:
    def __init__(self, dados_origem, dados_destino, comunicador):
        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.fabricantes_encontrados_tratados = None
        self.fabricantes_nencontrados_tratados = None

    def inicia_fabricantes(self, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        fabricante_origem = iterador.select_fabricante_origem()
        fabricante_destino = iterador.select_fabricante_destino()

        if apagado['apagado'] == 'sim':
            for fabricante in fabricante_origem:
                if fabricante['apagado'] == 'S':
                    fabricante_origem.remove(fabricante)
                else:
                    continue

        fabricante = self.procura_fabricantes(fabricante_origem, fabricante_destino)
        self.fabricantes_encontrados_tratados = self.tratamento_fabricantes(fabricante['fabricantes_encontrados'])
        self.fabricantes_nencontrados_tratados = self.tratamento_fabricantes(fabricante['fabricantes_nencontrados'])
        fabricantes_log = iterador.insert_fabricante(self.fabricantes_nencontrados_tratados)

        return fabricantes_log

    def procura_fabricantes(self, fabricante_origem, fabricante_destino):
        fabricantes_encontrados = []
        fabricantes_nencontrados = []

        for fabricante in fabricante_origem:
            novo_id = self.retorna_fabricante(fabricante['cnpj'], fabricante_destino)

            if novo_id:
                fabricante.update({'novo_id': novo_id})
                fabricantes_encontrados.append(fabricante)
            else:
                fabricante.update({'novo_id': None})
                fabricantes_nencontrados.append(fabricante)

        return {'fabricantes_encontrados': fabricantes_encontrados,
                'fabricantes_nencontrados': fabricantes_nencontrados}

    @staticmethod
    def retorna_fabricante(cnpj_origem, fabricante_destino):
        for fabricante in fabricante_destino:
            cnpj_destino = fabricante['cnpj']
            id_fabricante = int(fabricante['id_fabricante'])
            if cnpj_origem == cnpj_destino:
                return id_fabricante
            else:
                continue

    def tratamento_fabricantes(self, fabricantes):
        for fabricante in fabricantes:
            fabricante.update({'comunicador': self.comunicador})

        return fabricantes

    def retorna_fabricantes_tratados(self):
        fabricantes_encontrados_tratados = self.fabricantes_encontrados_tratados
        return fabricantes_encontrados_tratados
