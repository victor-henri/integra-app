from iteradorSQL import IteradorSql


class Cliente:
    def __init__(self, dados_origem, dados_destino, empresas_selecionadas, comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.empresas_selecionadas = empresas_selecionadas
        self.comunicador = comunicador
        self.clientes_selecionados = None

    def inicia_clientes(self, apagado):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)
        clientes = iterador.select_cliente(self.empresas_selecionadas)

        if apagado['apagado'] == 'sim':
            clientes = self.remove_apagado(clientes)

        clientes_tratados = self.trata_clientes(clientes)
        self.clientes_selecionados = self.separa_clientes_ids(clientes_tratados)
        clientes_log = iterador.insert_cliente(clientes_tratados)

        return clientes_log

    def trata_clientes(self, clientes):

        for cliente in clientes:
            datas = {'data_nascimento': cliente['data_nascimento'],
                     'data_cadastro': cliente['data_cadastro'],
                     'data_alteracao': cliente['data_alteracao']}

            campos_especiais = {'nome': cliente['nome'],
                                'endereco': cliente['endereco']}

            datas_tratadas = self.trata_campo_data(datas)
            campos_tratados = self.trata_campo_especial(campos_especiais)

            cliente.update({'data_nascimento': datas_tratadas['data_nascimento']})
            cliente.update({'data_cadastro': datas_tratadas['data_cadastro']})
            cliente.update({'data_alteracao': datas_tratadas['data_alteracao']})
            cliente.update({'nome': campos_tratados['nome']})
            cliente.update({'endereco': campos_tratados['endereco']})
            cliente.update({'comunicador': self.comunicador})

        return clientes

    @staticmethod
    def remove_apagado(clientes):

        for registro in clientes:
            if registro['apagado'] == 'S':
                clientes.remove(registro)
            else:
                continue

        return clientes

    @staticmethod
    def trata_campo_data(datas):

        for chave, data in datas.items():
            if data is None:
                pass
            else:
                data_formatada = data.strftime('%Y-%m-%d')
                datas.update({chave: data_formatada})
        return datas

    @staticmethod
    def trata_campo_especial(campos_especiais):

        caracteres = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                      'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ')

        for chave, campo in campos_especiais.items():
            if campo is None:
                pass
            else:
                valores = []
                for caracter in campo:
                    if caracter in caracteres:
                        valores.append(caracter)
                campo_formatado = ''.join(valores)
                campos_especiais.update({chave: campo_formatado})
        return campos_especiais

    @staticmethod
    def separa_clientes_ids(clientes):

        clientes_selecionados_l = []

        for cliente in clientes:
            clientes_selecionados_l.append(cliente['id_cliente'])
        clientes_selecionados = tuple(clientes_selecionados_l)

        return clientes_selecionados

    def retorna_clientes_ids(self):
        return self.clientes_selecionados
