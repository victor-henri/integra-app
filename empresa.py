from iteradorSQL import IteradorSql


class Empresa:
    def __init__(self, dados_origem, dados_destino, empresas_selecionadas, comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.empresas_selecionadas = empresas_selecionadas
        self.comunicador = comunicador

    def inicia_empresas(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        empresas = iterador.select_empresas(self.empresas_selecionadas)

        if apagado['apagado'] == 'sim':
            empresas = self.remove_apagado(empresas)

        empresas_tratadas = self.trata_empresas(empresas)
        empresas_log = iterador.insert_empresa(empresas_tratadas)

        return empresas_log

    def trata_empresas(self, empresas):

        for empresa in empresas:
            empresa.update({'comunicador': self.comunicador})

        return empresas

    @staticmethod
    def remove_apagado(empresas):

        for registro in empresas:
            if registro['apagado'] == 'S':
                empresas.remove(registro)
            else:
                continue

        return empresas
