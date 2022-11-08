from iteradorSQL import IteradorSql
from datetime import datetime


class Produto:

    def __init__(self,
                 fabricantes_encontrados_tratados,
                 principios_encontrados_tratados,
                 id_fabricante,
                 id_principio,
                 grupos_selecionados,
                 dados_origem,
                 dados_destino,
                 comunicador):

        self.dados_origem = dados_origem
        self.dados_destino = dados_destino
        self.comunicador = comunicador
        self.principios_encontrados_tratados = principios_encontrados_tratados
        self.fabricantes_encontrados_tratados = fabricantes_encontrados_tratados
        self.id_fabricante = id_fabricante
        self.id_principio = id_principio
        self.grupos_selecionados = grupos_selecionados
        self.produtos_pre_insert = None
        self.produtos_ids_separados = None

    def inicia_produtos(self, marcador_produto, apagado):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        iterador.conexao_destino(self.dados_destino)

        produtos_origem = iterador.select_produto()

        if apagado['apagado'] == 'sim':
            for produto in produtos_origem:
                if produto['apagado'] == 'S':
                    produtos_origem.remove(produto)
                else:
                    continue

        produtos_processamento = self.separa_produtos_selecionados(produtos_origem, self.grupos_selecionados)

        if marcador_produto['remover_produtos_barras_zerados'] == 'sim':
            quantidade_zeros = marcador_produto['quantidade_zeros_barras']
            produtos_processamento = self.remove_produtos_barras_zerados(produtos_processamento, quantidade_zeros)
        if marcador_produto['fabricante_por_cnpj'] == 'sim':
            produtos_processamento = self.atualizacao_fabricantes_por_cnpj(produtos_processamento)
        if marcador_produto['fabricante_por_id'] == 'sim':
            produtos_processamento = self.atualizacao_fabricantes_por_id(produtos_processamento)
        if marcador_produto['principio_por_desc'] == 'sim':
            produtos_processamento = self.atualizacao_principio_por_desc(produtos_processamento)
        if marcador_produto['principio_por_id'] == 'sim':
            produtos_processamento = self.atualizacao_principio_por_id(produtos_processamento)

        self.produtos_pre_insert = self.tratamento_produtos(produtos_processamento)

        self.produtos_ids_separados = self.separa_produtos_ids(self.produtos_pre_insert)
        produtos_log = iterador.insert_produto(self.produtos_pre_insert)
        self.atualizacao_pos_insert()
        return produtos_log

    def separa_produtos_selecionados(self, produtos_origem, grupos_selecionados):
        lista_grupos = []  # Saída → Lista

        for grupo in grupos_selecionados:
            lista_grupos.append(int(grupo['antigo_id']))

        produtos_selecionados = []  # Saída → Lista de Dicionários.
        for produto in produtos_origem:
            atual_grupo_id = int(produto['id_grupo'])
            if atual_grupo_id in lista_grupos:
                produtos_selecionados.append(produto)
            else:
                continue

        for produto in produtos_selecionados:
            atual_id = int(produto['id_grupo'])
            novo_id = self.retorna_grupo(atual_id, grupos_selecionados)
            produto['id_grupo'] = novo_id

        return produtos_selecionados

    @staticmethod
    def retorna_grupo(atual_id, grupos_selecionados):
        for grupo in grupos_selecionados:
            antigo_id = int(grupo['antigo_id'])
            novo_id = int(grupo['novo_id'])
            if atual_id == antigo_id:
                return novo_id
            else:
                continue

    def remove_produtos_barras_zerados(self, produtos, quantidade_zeros):
        for produto in produtos:
            retorno = self.conta_zeros(produto['barras'], quantidade_zeros)
            if retorno is True:
                produtos.remove(produto)
            else:
                continue

        return produtos

    @staticmethod
    def conta_zeros(barras, quantidade_zeros):
        contador = 0
        zeros = ''

        while contador < quantidade_zeros:
            zeros += '0'
            contador += 1

        corte = barras[:quantidade_zeros]
        resultado = zeros in corte

        return resultado

    def atualizacao_fabricantes_por_cnpj(self, produtos):
        for produto in produtos:

            if produto['id_fabricante'] is None:
                produto['id_fabricante_ant'] = None
            else:
                atual_id = int(produto['id_fabricante'])
                novo_id = self.retorna_novoid_fabricante(atual_id)

                if novo_id:
                    produto.update({'id_fabricante': novo_id, 'id_fabricante_ant': None})
                else:
                    produto.update({'id_fabricante_ant': atual_id, 'id_fabricante': None})

        return produtos

    def retorna_novoid_fabricante(self, atual_id):
        for fabricante in self.fabricantes_encontrados_tratados:
            fabricante_id = int(fabricante['id_fabricante'])
            novo_id = int(fabricante['novo_id'])
            if atual_id == fabricante_id:
                return novo_id
            else:
                continue

    def atualizacao_fabricantes_por_id(self, produtos):
        for produto in produtos:
            produto['id_fabricante'] = int(self.id_fabricante)

        return produtos

    def atualizacao_principio_por_desc(self, produtos):
        for produto in produtos:

            if produto['id_principio_ativo'] is None:
                produto['id_principio_ant'] = None
            else:
                atual_id = int(produto['id_principio_ativo'])
                novo_id = self.retorna_novo_id_principios(atual_id)

                if novo_id:
                    produto.update({'id_principio_ativo': novo_id, 'id_principio_ant': None})
                else:
                    produto.update({'id_principio_ant': atual_id, 'id_principio_ativo': None})

        return produtos

    def retorna_novo_id_principios(self, atual_id):
        for principio in self.principios_encontrados_tratados:
            principio_ativo_id = int(principio['id_principio_ativo'])
            if atual_id == principio_ativo_id:
                return principio_ativo_id
            else:
                continue

    def atualizacao_principio_por_id(self, produtos):
        for produto in produtos:
            produto['id_principio_ativo'] = int(self.id_principio)

        return produtos

    def tratamento_produtos(self, produtos):
        for produto in produtos:

            datas = {'inicio_promocao': produto['inicio_promocao'],
                     'final_promocao': produto['final_promocao'],
                     'data_cadastro': produto['data_cadastro'],
                     'data_alteracao': produto['data_alteracao']}

            datas_tratadas = self.trata_campo_data(datas)

            produto.update({'inicio_promocao': datas_tratadas['inicio_promocao']})
            produto.update({'final_promocao': datas_tratadas['final_promocao']})
            produto.update({'data_cadastro': datas_tratadas['data_cadastro']})
            produto.update({'data_alteracao': datas_tratadas['data_alteracao']})
            produto.update({'comunicador': self.comunicador})

        return produtos

    @staticmethod
    def trata_campo_data(datas):
        for chave, data in datas.items():
            if data is None:
                pass
            else:
                if data == '0000-00-00':
                    nova_data = datetime(1899, 12, 30)
                    data_formatada = nova_data.strftime('%Y-%m-%d')
                    datas.update({chave: data_formatada})
                else:
                    data_formatada = data.strftime('%Y-%m-%d')
                    datas.update({chave: data_formatada})
        return datas

    @staticmethod
    def separa_produtos_ids(produtos_processados):
        lista_produtos_ids = []

        for produto in produtos_processados:
            produto_id = int(produto['id_produto'])
            lista_produtos_ids.append(produto_id)

        return lista_produtos_ids

    def retorna_produtos_ids(self):
        produtos_ids_separados = self.produtos_ids_separados
        return produtos_ids_separados

    def atualizacao_pos_insert(self):
        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)

        tabela_produto = {'tabela': 'produto'}
        tabela_fabricante = {'tabela': 'fabricante'}
        tabela_principio = {'tabela': 'principio_ativo'}

        produtos_pos_insert = iterador.consulta_pos_insert(tabela_produto)
        fabricantes_pos_insert = iterador.consulta_pos_insert(tabela_fabricante)
        principio_pos_insert = iterador.consulta_pos_insert(tabela_principio)

        for produto in self.produtos_pre_insert:
            produto_id = int(produto['id_produto'])
            novo_produto_id = self.retorna_id_produto_pos_insert(produto_id, produtos_pos_insert)

            if produto['id_fabricante_ant'] is None:
                pass
            else:
                fabricante_id = int(produto['id_fabricante_ant'])
                novo_fabricante_id = self.retorna_id_fabricante_pos_insert(fabricante_id, fabricantes_pos_insert)
                dados_fabricante = {'campo': 'fabricante',
                                    'valor': novo_fabricante_id,
                                    'id_produto': novo_produto_id}
                iterador.atualiza_campo_produto_pos_insert(dados_fabricante)

            if produto['id_principio_ant'] is None:
                pass
            else:
                principio_id = int(produto['id_principio_ant'])
                novo_principio_id = self.retorna_id_principio_pos_insert(principio_id, principio_pos_insert)
                dados_principio = {'campo': 'principio_ativo',
                                   'valor': novo_principio_id,
                                   'id_produto': novo_produto_id}
                iterador.atualiza_campo_produto_pos_insert(dados_principio)

    @staticmethod
    def retorna_id_produto_pos_insert(produto_id, produtos_pos_insert):
        for produto in produtos_pos_insert:
            antigo_produto_id = int(produto['campo_auxiliar'])
            novo_produto_id = int(produto['id_produto'])
            if produto_id == antigo_produto_id:
                return novo_produto_id
            else:
                continue

    @staticmethod
    def retorna_id_fabricante_pos_insert(fabricante_id, fabricantes_pos_insert):
        for fabricante in fabricantes_pos_insert:
            antigo_fabricante_id = int(fabricante['campo_auxiliar'])
            novo_fabricante_id = int(fabricante['id_fabricante'])
            if fabricante_id == antigo_fabricante_id:
                return novo_fabricante_id
            else:
                continue

    @staticmethod
    def retorna_id_principio_pos_insert(principio_id, principio_pos_insert):
        for principio in principio_pos_insert:
            antigo_principio_id = int(principio['campo_auxiliar'])
            novo_principio_id = int(principio['id_principio_ativo'])
            if principio_id == antigo_principio_id:
                return novo_principio_id
            else:
                continue
