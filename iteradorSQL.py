import pymysql
import SQLs


class IteradorSql:
    def __init__(self):
        self.origem_conexao = None
        self.destino_conexao = None

    def conexao_origem(self, dados_origem):
        try:
            self.origem_conexao = pymysql.connect(host=dados_origem['host'],
                                                  user=dados_origem['user'],
                                                  password=dados_origem['password'],
                                                  database=dados_origem['database'],
                                                  port=dados_origem['port'],
                                                  charset='utf8',
                                                  sql_mode="NO_ENGINE_SUBSTITUTION",
                                                  cursorclass=pymysql.cursors.DictCursor)

            return {'retorno': 'Conectado', 'descricao': self.origem_conexao}

        except pymysql.err.OperationalError as err:
            return {'retorno': 'pymysql.err.OperationalError', 'codigo': err.args[0], 'descricao': err.args[1]}

        except Exception as err:
            return {'retorno': 'Exception', 'codigo': err.args[0], 'descricao': err.args[1]}

    def conexao_destino(self, dados_destino):
        try:
            self.destino_conexao = pymysql.connect(host=dados_destino['host'],
                                                   user=dados_destino['user'],
                                                   password=dados_destino['password'],
                                                   database=dados_destino['database'],
                                                   port=dados_destino['port'],
                                                   charset='latin1',
                                                   sql_mode="NO_ENGINE_SUBSTITUTION",
                                                   cursorclass=pymysql.cursors.DictCursor)

            return {'retorno': 'Conectado', 'descricao': self.destino_conexao}

        except pymysql.err.OperationalError as err:
            return {'retorno': 'pymysql.err.OperationalError', 'codigo': err.args[0], 'descricao': err.args[1]}

        except Exception as err:
            return {'retorno': 'Exception', 'codigo': err.args[0], 'descricao': err.args[1]}

    def select_produto(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_produto)
        produto = cursor_origem.fetchall()

        return produto

    def insert_produto(self, produtos):
        cursor_destino = self.destino_conexao.cursor()
        produtos_log = []

        for produto in produtos:
            try:
                cursor_destino.execute(SQLs.query_insert_produto, produto)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Produto ID: {produto['id_produto']} " \
                                f"| Descrição: {produto['descricao']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                produto_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                produtos_log.append(produto_log)
                continue
            except Exception as err:
                registro_erro = f"Produto ID: {produto['id_produto']} " \
                                f"| Descrição: {produto['descricao']} não importado."
                retorno_erro = f"Descrição: {err}"
                produto_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                produtos_log.append(produto_log)
                continue

        return produtos_log

    def consulta_produto_pos_insert(self, dados_tabela):
        cursor_destino = self.destino_conexao.cursor()

        if dados_tabela['tabela'] == 'produto':
            cursor_destino.execute('SELECT id_produto, campo_auxiliar '
                                   'FROM produto '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = cursor_destino.fetchall()

        elif dados_tabela['tabela'] == 'fabricante':
            cursor_destino.execute('SELECT id_fabricante, campos_auxiliar '
                                   'FROM fabricante '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = cursor_destino.fetchall()

        elif dados_tabela['tabela'] == 'principio_ativo':
            cursor_destino.execute('SELECT id_principio_ativo, campo_auxiliar '
                                   'FROM principio_ativo '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = cursor_destino.fetchall()

        return dados_pos_insert

    def atualiza_campo_produto_pos_insert(self, dados_atualizacao):
        cursor_destino = self.destino_conexao.cursor()

        if dados_atualizacao['campo'] == 'fabricante':
            cursor_destino.execute('UPDATE produto '
                                   'SET id_fabricante = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', dados_atualizacao)

        else:
            cursor_destino.execute('UPDATE produto '
                                   'SET id_principio_ativo = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', dados_atualizacao)

    def select_fabricante_origem(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_fabricante)
        fabricante = cursor_origem.fetchall()

        return fabricante

    def select_fabricante_destino(self):
        cursor_destino = self.destino_conexao.cursor()
        cursor_destino.execute(SQLs.query_select_fabricante)
        fabricante = cursor_destino.fetchall()

        return fabricante

    def insert_fabricante(self, fabricantes):
        cursor_destino = self.destino_conexao.cursor()
        fabricantes_log = []

        for fabricante in fabricantes:
            try:
                cursor_destino.execute(SQLs.query_insert_fabricante, fabricante)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Fabricante ID: {fabricante['id_fabricante']} " \
                                f"| Descrição: {fabricante['descricao']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                fabricante_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                fabricantes_log.append(fabricante_log)
                continue
            except Exception as err:
                registro_erro = f"Fabricante ID: {fabricante['id_fabricante']} " \
                                f"| Descrição: {fabricante['descricao']} não importado."
                retorno_erro = f"Descrição: {err}"
                fabricante_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                fabricantes_log.append(fabricante_log)
                continue

        return fabricantes_log

    def select_principio_ativo_origem(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_principio)
        principio_ativo = cursor_origem.fetchall()

        return principio_ativo

    def select_principio_ativo_destino(self):
        cursor_destino = self.destino_conexao.cursor()
        cursor_destino.execute(SQLs.query_select_principio)
        principio_ativo = cursor_destino.fetchall()

        return principio_ativo

    def insert_principios(self, principios):
        cursor_destino = self.destino_conexao.cursor()
        principios_log = []

        for principio in principios:
            try:
                cursor_destino.execute(SQLs.query_insert_principio, principio)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Principio Ativo ID: {principio['id_principio_ativo']} " \
                                f"| Descrição: {principio['descricao']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                principio_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                principios_log.append(principio_log)
                continue
            except Exception as err:
                registro_erro = f"Principio Ativo ID: {principio['id_principio_ativo']} " \
                                f"| Descrição: {principio['descricao']} não importado."
                retorno_erro = f"Descrição: {err}"
                principio_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                principios_log.append(principio_log)
                continue

        return principios_log

    def select_barras(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_barras)
        barras = cursor_origem.fetchall()

        return barras

    def insert_barras(self, barras_selecionados):
        cursor_destino = self.destino_conexao.cursor()
        barras_log = []

        for barras in barras_selecionados:
            try:
                cursor_destino.execute(SQLs.query_insert_barras, barras)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Barras do Produto ID: {barras['id_produto']} " \
                                f"| Barras: {barras['barras']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                barra_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                barras_log.append(barra_log)
                continue
            except Exception as err:
                registro_erro = f"Barras do Produto ID: {barras['id_produto']} " \
                                f"| Barras: {barras['barras']} não importado."
                retorno_erro = f"Descrição: {err}"
                barra_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                barras_log.append(barra_log)
                continue

        return barras_log

    def select_estoque(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_estoque)
        estoque = cursor_origem.fetchall()

        return estoque

    def insert_estoque(self, estoques):
        cursor_destino = self.destino_conexao.cursor()
        estoques_log = []

        for estoque in estoques:
            try:
                cursor_destino.execute(SQLs.query_insert_estoque, estoque)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Estoque do Produto ID: {estoque['id_produto']} " \
                                f"| Estoque: {estoque['estoque']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                estoque_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                estoques_log.append(estoque_log)
                continue
            except Exception as err:
                registro_erro = f"Estoque do Produto ID: {estoque['id_produto']} " \
                                f"| Estoque: {estoque['estoque']} não importado."
                retorno_erro = f"Descrição: {err}"
                estoque_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                estoques_log.append(estoque_log)
                continue

        return estoques_log

    def select_produto_pos_insert(self):
        cursor_destino = self.destino_conexao.cursor()
        cursor_destino.execute('SELECT id_produto, campo_auxiliar FROM produto;')
        produto = cursor_destino.fetchall()

        return produto

    def select_lote(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_lote)
        lote = cursor_origem.fetchall()

        return lote

    def insert_lote(self, lotes):
        cursor_destino = self.destino_conexao.cursor()
        lotes_log = []

        for lote in lotes:
            try:
                cursor_destino.execute(SQLs.query_insert_lote, lote)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Lote do Produto ID: {lote['id_produto']} " \
                                f"| Lote: {lote['lote_descricao']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                lote_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                lotes_log.append(lote_log)
                continue
            except Exception as err:
                registro_erro = f"Lote do Produto ID: {lote['id_produto']} " \
                                f"| Lote: {lote['lote_descricao']} não importado."
                retorno_erro = f"Descrição: {err}"
                lote_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                lotes_log.append(lote_log)
                continue

        return lotes_log

    def select_preco_filial(self):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_preco)
        preco_filial = cursor_origem.fetchall()

        return preco_filial

    def insert_precos_filial(self, preco_filial):
        cursor_destino = self.destino_conexao.cursor()
        preco_filial_log = []

        for preco in preco_filial:
            try:
                cursor_destino.execute(SQLs.query_insert_preco, preco)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Preço Filial do Produto ID: {preco['id_produto']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                preco_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                preco_filial_log.append(preco_log)
                continue
            except Exception as err:
                registro_erro = f"Preço Filial do Produto ID: {preco['id_produto']} não importado."
                retorno_erro = f"Descrição: {err}"
                preco_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                preco_filial_log.append(preco_log)
                continue

        return preco_filial_log

    def select_empresas(self, empresas_selecionadas):
        cursor_origem = self.origem_conexao.cursor()

        cursor_origem.execute(SQLs.query_select_empresa, (empresas_selecionadas,))
        empresa = cursor_origem.fetchall()  # → Lista de Dicionários.

        return empresa

    def select_fornecedor_origem(self, fornecedores_selecionados):
        cursor_origem = self.origem_conexao.cursor()
        cursor_origem.execute(SQLs.query_select_fornecedor_origem, (fornecedores_selecionados,))
        fornecedor = cursor_origem.fetchall()

        return fornecedor

    def select_fornecedor_destino(self):
        cursor_destino = self.destino_conexao.cursor()
        cursor_destino.execute(SQLs.query_select_fornecedor_destino)
        fornecedor = cursor_destino.fetchall()

        return fornecedor

    def select_cliente(self, empresas_selecionadas):
        cursor = self.origem_conexao.cursor()

        cursor.execute(SQLs.query_select_cliente, (empresas_selecionadas,))
        cliente = cursor.fetchall()  # → Lista de Dicionários.

        return cliente

    def insert_empresa(self, empresas):
        cursor = self.destino_conexao.cursor()
        empresas_log = []

        for empresa in empresas:
            try:
                cursor.execute(SQLs.query_insert_empresa, empresa)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Empresa ID: {empresa['id_empresa']} | Nome: {empresa['nome_fantasia']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                empresa_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                empresas_log.append(empresa_log)
                continue
            except Exception as err:
                registro_erro = f"Empresa ID: {empresa['id_empresa']} | Nome: {empresa['nome_fantasia']} não importado."
                retorno_erro = f"Descrição: {err}"
                empresa_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                empresas_log.append(empresa_log)
                continue

        return empresas_log

    def insert_fornecedor(self, fornecedores):
        cursor = self.destino_conexao.cursor()
        fornecedores_log = []

        for fornecedor in fornecedores:
            try:
                cursor.execute(SQLs.query_insert_fornecedor, fornecedor)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Fornecedor ID: {fornecedor['id_fornecedor']} " \
                                f"| Nome: {fornecedor['nome_fantasia']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                fornecedor_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                fornecedores_log.append(fornecedor_log)
                continue
            except Exception as err:
                registro_erro = f"Fornecedor ID: {fornecedor['id_fornecedor']} " \
                                f"| Nome: {fornecedor['nome_fantasia']} não importado."
                retorno_erro = f"Descrição: {err}"
                fornecedor_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                fornecedores_log.append(fornecedor_log)
                continue

        return fornecedores_log

    def insert_cliente(self, clientes):
        cursor = self.destino_conexao.cursor()
        clientes_log = []

        for cliente in clientes:
            try:
                cursor.execute(SQLs.query_insert_cliente, cliente)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Cliente ID: {cliente['id_cliente']} | Nome: {cliente['nome']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                cliente_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                clientes_log.append(cliente_log)
                continue
            except Exception as err:
                registro_erro = f"Cliente ID: {cliente['id_cliente']} | Nome: {cliente['nome']} não importado."
                retorno_erro = f"Descrição: {err}"
                cliente_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                clientes_log.append(cliente_log)
                continue

        # Atualiza o id_empresa da tabela cliente com os novos ids de empresas inseridas
        cursor.execute('UPDATE cliente '
                       'INNER JOIN empresa '
                       'ON cliente.campo_auxiliar = empresa.campo_auxiliar '
                       'SET cliente.id_empresa = empresa.id_empresa;')

        return clientes_log

    def insert_receber(self, recebers):
        cursor_destino = self.destino_conexao.cursor()
        recebers_log = []

        for receber in recebers:
            try:
                cursor_destino.execute(SQLs.query_insert_receber, receber)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Receber do Cliente ID: {receber['id_cliente']} " \
                                f"| Valor: {receber['valor']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                receber_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                recebers_log.append(receber_log)
                continue
            except Exception as err:
                registro_erro = f"Receber do Cliente ID: {receber['id_cliente']} " \
                                f"| Valor: {receber['valor']} não importado."
                retorno_erro = f"Descrição: {err}"
                receber_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                recebers_log.append(receber_log)
                continue

        # Atualiza o clientes_id da tabela receber com os novos ids de clientes inseridos a partir do
        # campo lojas_leram2 que recebeu o clientes_id do banco de origem.
        cursor_destino.execute('UPDATE contas_receber '
                               'INNER JOIN cliente '
                               'ON contas_receber.campo_auxiliar = cliente.campo_auxiliar '
                               'SET contas_receber.id_cliente = cliente.id_cliente;')

        # Atualiza o empresa_id da tabela receber com os novos ids de empresas.
        cursor_destino.execute('UPDATE contas_receber '
                               'INNER JOIN cliente '
                               'ON contas_receber.id_cliente = cliente.id_cliente '
                               'SET contas_receber.id_empresa = cliente.id_empresa;')

        return recebers_log

    def consulta_fornecedor_pos_insert(self):
        cursor_destino = self.destino_conexao.cursor()
        cursor_destino.execute(SQLs.query_consulta_pos_insert_fornecedor)
        fornecedores = cursor_destino.fetchall()

        return fornecedores

    def consulta_pos_insert(self, produto):
        cursor_destino = self.destino_conexao.cursor()

        if produto['tabela'] == 'produto':
            cursor_destino.execute(SQLs.query_consulta_pos_insert_produto)
            consulta_pos_insert = cursor_destino.fetchall()

        elif produto['tabela'] == 'fabricante':
            cursor_destino.execute(SQLs.query_consulta_pos_insert_fabricante)
            consulta_pos_insert = cursor_destino.fetchall()

        else:
            cursor_destino.execute(SQLs.query_consulta_pos_insert_principio)
            consulta_pos_insert = cursor_destino.fetchall()

        return consulta_pos_insert

    def insert_pagar(self, pagars):
        cursor_destino = self.destino_conexao.cursor()
        pagars_log = []

        for pagar in pagars:
            try:
                cursor_destino.execute(SQLs.query_insert_pagar, pagar)
            except UnicodeEncodeError as uni_err:
                registro_erro = f"Pagar do Fornece NF: {pagar['nota_fiscal']} " \
                                f"| Valor: {pagar['valor']} não importado."
                retorno_erro = f"Erro na codificação de caracteres - Descrição: {uni_err}"
                pagar_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                pagars_log.append(pagar_log)
                continue
            except Exception as err:
                registro_erro = f"Pagar do Fornece NF: {pagar['nota_fiscal']} " \
                                f"| Valor: {pagar['valor']} não importado."
                retorno_erro = f"Descrição: {err}"
                pagar_log = {'registro_erro': registro_erro, 'retorno_erro': retorno_erro}
                pagars_log.append(pagar_log)
                continue

        return pagars_log

    def select_receber(self, clientes_selecionados):
        cursor_origem = self.origem_conexao.cursor()

        cursor_origem.execute(SQLs.query_select_receber, (clientes_selecionados,))
        receber = cursor_origem.fetchall()  # → Lista de Dicionários.

        return receber

    def select_pagar(self, fornecedores_selecionados):
        cursor_origem = self.origem_conexao.cursor()

        cursor_origem.execute(SQLs.query_select_pagar, (fornecedores_selecionados,))
        pagar = cursor_origem.fetchall()  # → Lista de Dicionários.

        return pagar

    def select_grupo_origem_sapagado(self):
        cursor = self.origem_conexao.cursor()

        cursor.execute('SELECT id_grupo, descricao FROM grupo WHERE apagado = "N";')
        grupo = cursor.fetchall()

        return grupo

    def select_grupo_origem_capagado(self):
        cursor = self.origem_conexao.cursor()

        cursor.execute('SELECT id_grupo, descricao FROM grupo;')
        grupo = cursor.fetchall()

        return grupo

    def select_grupo_destino_sapagado(self):
        cursor = self.destino_conexao.cursor()

        cursor.execute('SELECT id_grupo, descricao FROM grupo WHERE apagado = "N";')
        grupo = cursor.fetchall()

        return grupo

    def select_grupo_destino_capagado(self):
        cursor = self.destino_conexao.cursor()

        cursor.execute('SELECT id_grupo, descricao FROM grupo;')
        grupo = cursor.fetchall()

        return grupo

    def select_listagem_empresa(self):
        cursor = self.origem_conexao.cursor()

        cursor.execute('SELECT id_empresa, nome_fantasia FROM empresa;')
        empresa = cursor.fetchall()  # Saída → Lista de Dicionários.

        return empresa

    def select_listagem_fornecedor(self):
        cursor = self.origem_conexao.cursor()

        cursor.execute('SELECT id_fornecedor, razao_social FROM fornecedor;')
        fornecedor = cursor.fetchall()  # Saída → Lista de Dicionários.

        return fornecedor
