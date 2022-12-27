from interfaces.repository import RepositoryInterface
from mariadb_connection import ConnectionMariaDb
from typing import Type
import pymysql
import SQLs


class RepositoryMariaDb(RepositoryInterface):
    """_summary_

    Args:
        RepositoryInterface (_type_): _description_
    """

    def __init__(self, connection: Type[ConnectionMariaDb]):
        self.__connection = connection
        self.__cursor = None

    def create_cursor(self) -> None:
        """_summary_
        """
        self.__cursor = self.__connection.cursor()

    def __unicode_error(self, data: dict, error: UnicodeEncodeError) -> dict:
        error_register = f"{data['first_column']}: {data['first_value']}" \
                            f" | {data['second_column']}: {data['second_value']} não importado."
        error_return = f"Erro na codificação de caracteres - Descrição: {error}"
        log = {'registro_erro': error_register, 'retorno_erro': error_return}

        return log

    def __exception_error(self, data: dict, error: Exception) -> dict:
        error_register = f"{data['first_column']}: {data['first_value']}" \
                         f" | {data['second_column']}: {data['second_value']} não importado."
        error_return = f"Descrição: {error}"
        log = {'registro_erro': error_register, 'retorno_erro': error_return}

        return log

    def select_produto(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_produto)
        product = self.__cursor.fetchall()

        return product

    def insert_produto(self, products):
        # Destino

        product_logs = []
        for product in products:
            data = {'first_column': 'id_produto',
                    'first_value': product['id_produto'],
                    'second_column': 'descricao',
                    'second_value': product['descricao']}

            if product['novo_id'] is None:
                try:
                    self.__cursor.execute(SQLs.query_insert_produto, product)

                except UnicodeEncodeError as error:
                    log = self.__unicode_error(data, error)
                    product_logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    product_logs.append(log)
                    continue
            else:
                continue

        return product_logs

    def consulta_produto_pos_insert(self, dados_tabela):
        # Destino

        if dados_tabela['tabela'] == 'produto':
            self.__cursor.execute('SELECT id_produto, campo_auxiliar '
                                   'FROM produto '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = self.__cursor.fetchall()

        elif dados_tabela['tabela'] == 'fabricante':
            self.__cursor.execute('SELECT id_fabricante, campos_auxiliar '
                                   'FROM fabricante '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = self.__cursor.fetchall()

        elif dados_tabela['tabela'] == 'principio_ativo':
            self.__cursor.execute('SELECT id_principio_ativo, campo_auxiliar '
                                   'FROM principio_ativo '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            dados_pos_insert = self.__cursor.fetchall()

        return dados_pos_insert

    def atualiza_campo_produto_pos_insert(self, dados_atualizacao):
        # Destino

        if dados_atualizacao['campo'] == 'fabricante':
            self.__cursor.execute('UPDATE produto '
                                   'SET id_fabricante = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', dados_atualizacao)

        else:
            self.__cursor.execute('UPDATE produto '
                                   'SET id_principio_ativo = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', dados_atualizacao)

    def select_fabricante_origem(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_fabricante)
        manufacturer = self.__cursor.fetchall()

        return manufacturer

    # def select_fabricante_destino(self):
    #     # Destino
    #     # Remover este método

    #     self.__cursor.execute(SQLs.query_select_fabricante)
    #     manufacturer = self.__cursor.fetchall()

    #     return manufacturer

    def insert_fabricante(self, manufacturers):
        # Destino

        manufacturer_logs = []
        for manufacturer in manufacturers:
            data = {'first_column': 'id_fabricante',
                    'first_value': manufacturer['id_fabricante'],
                    'second_column': 'descricao',
                    'second_value': manufacturer['descricao']}

            try:
                self.__cursor.execute(SQLs.query_insert_fabricante, manufacturer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                manufacturer_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                manufacturer_logs.append(log)
                continue

        return manufacturer_logs

    def select_principio_ativo_origem(self):
        # Origem

        self.__cursor.execute(SQLs.query_select_principio)
        principle = self.__cursor.fetchall()

        return principle

    # def select_principio_ativo_destino(self):
    #     # Destino
    #     # Remover este metodo

    #     self.__cursor.execute(SQLs.query_select_principio)
    #     principio_ativo = self.__cursor.fetchall()

    #     return principio_ativo

    def insert_principios(self, principles):
        # Destino

        principle_logs = []
        for principle in principles:
            data = {'first_column': 'id_principio_ativo',
                    'first_value': principle['id_principio_ativo'],
                    'second_column': 'descricao',
                    'second_value': principle['descricao']}

            try:
                self.__cursor.execute(SQLs.query_insert_principio, principle)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                principle_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                principle_logs.append(log)
                continue

        return principle_logs

    def select_barras(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_barras)
        bars = self.__cursor.fetchall()

        return bars

    def insert_barras(self, bars):
        # Destino

        bar_logs = []
        for item in bars:
            data = {'first_column': 'id_produto',
                    'first_value': item['id_produto'],
                    'second_column': 'barras',
                    'second_value': item['barras']}

            try:
                self.__cursor.execute(SQLs.query_insert_barras, item)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                bar_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                bar_logs.append(log)
                continue

        return bar_logs

    def select_estoque(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_estoque)
        stock = self.__cursor.fetchall()

        return stock

    def insert_estoque(self, stocks):
        # Destino

        stock_logs = []

        for stock in stocks:
            data = {'first_column': 'id_produto',
                    'first_value': stock['id_produto'],
                    'second_column': 'estoque',
                    'second_value': stock['estoque']}

            if stock['existe'] == 'S':
                estoque_atual = int(stock['estoque'])
                try:
                    self.__cursor.execute(SQLs.query_select_atualizacao_estoque, stock)
                    estoque_existente = self.__cursor.fetchone()
                    estoque_existente.update({'estoque': estoque_existente['estoque'] + estoque_atual})
                    self.__cursor.execute(SQLs.query_update_estoque, estoque_existente)

                except UnicodeEncodeError as error:
                    log = self.__unicode_error(data, error)
                    stock_logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    stock_logs.append(log)
                    continue

            else:
                try:
                    self.__cursor.execute(SQLs.query_insert_estoque, stock)

                except UnicodeEncodeError as error:
                    log = self.__unicode_error(data, error)
                    stock_logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    stock_logs.append(log)
                    continue

        return stock_logs

    def select_produto_pos_insert(self):
        # Destino
        self.__cursor.execute('SELECT id_produto, campo_auxiliar FROM produto;')
        product = self.__cursor.fetchall()

        return product

    def select_lote(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_lote)
        partition = self.__cursor.fetchall()

        return partition

    def insert_lote(self, partitions):
        # Destino

        partition_logs = []
        for partition in partitions:
            data = {'first_column': 'id_produto',
                    'first_value': partition['id_produto'],
                    'second_column': 'lote_descricao',
                    'second_value': partition['lote_descricao']}

            try:
                self.__cursor.execute(SQLs.query_insert_lote, partition)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                partition_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                partition_logs.append(log)
                continue

        return partition_logs

    def select_preco_filial(self):
        # Origem
        self.__cursor.execute(SQLs.query_select_preco)
        price = self.__cursor.fetchall()

        return price

    def insert_precos_filial(self, prices):
        # Destino

        price_logs = []
        for price in prices:
            data = {'first_column': 'id_produto',
                    'first_value': price['id_produto'],
                    'second_column': 'id_produto',
                    'second_value': price['id_produto']}

            try:
                self.__cursor.execute(SQLs.query_insert_preco, price)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                price_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                price_logs.append(log)
                continue

        return price_logs

    def select_empresas(self, selected_companies):
        # Origem
        self.__cursor.execute(SQLs.query_select_empresa, (selected_companies,))
        company = self.__cursor.fetchall()

        return company

    def select_fornecedor_origem(self, selected_suppliers):
        # Origem
        self.__cursor.execute(SQLs.query_select_fornecedor_origem, (selected_suppliers,))
        supplier = self.__cursor.fetchall()

        return supplier

    def select_fornecedor_destino(self):
        # Destino
        self.__cursor.execute(SQLs.query_select_fornecedor_destino)
        supplier = self.__cursor.fetchall()

        return supplier

    def select_cliente(self, selected_companies):
        # Origem
        self.__cursor.execute(SQLs.query_select_cliente, (selected_companies,))
        customer = self.__cursor.fetchall()

        return customer

    def insert_empresa(self, companies):
        # Destino

        company_logs = []
        for company in companies:
            data = {'first_column': 'id_empresa',
                    'first_value': company['id_empresa'],
                    'second_column': 'nome_fantasia',
                    'second_value': company['nome_fantasia']}

            try:
                self.__cursor.execute(SQLs.query_insert_empresa, company)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                company_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                company_logs.append(log)
                continue

        return company_logs

    def insert_fornecedor(self, suppliers):
        # Destino

        supplier_logs = []
        for supplier in suppliers:
            data = {'first_column': 'id_fornecedor',
                    'first_value': supplier['id_fornecedor'],
                    'second_column': 'nome_fantasia',
                    'second_value': supplier['nome_fantasia']}

            try:
                self.__cursor.execute(SQLs.query_insert_fornecedor, supplier)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                supplier_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                supplier_logs.append(log)
                continue

        return supplier_logs

    def insert_cliente(self, customers):
        # Destino

        customer_logs = []
        for customer in customers:
            data = {'first_column': 'id_cliente',
                    'first_value': customer['id_cliente'],
                    'second_column': 'nome',
                    'second_value': customer['nome']}

            try:
                self.__cursor.execute(SQLs.query_insert_cliente, customer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                customer_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                customer_logs.append(log)
                continue

        # Atualiza o id_empresa da tabela cliente com os novos ids de empresas inseridas
        self.__cursor.execute(SQLs.query_update_cliente)

        return customer_logs

    def insert_receber(self, accounts):
        # Destino

        account_logs = []
        for account in accounts:
            data = {'first_column': 'id_cliente',
                    'first_value': account['id_cliente'],
                    'second_column': 'valor',
                    'second_value': account['valor']}

            try:
                self.__cursor.execute(SQLs.query_insert_receber, account)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                account_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                account_logs.append(log)
                continue

        # Atualiza o id_cliente da tabela receber com os novos ids de clientes inseridos a partir do
        # campo campo_auxiliar que recebeu o id_cliente do banco de origem.
        self.__cursor.execute(SQLs.query_atualiza_receber_cliente)

        # Atualiza o id_empresa da tabela receber com os novos ids de empresas.
        self.__cursor.execute(SQLs.query_atualiza_receber_empresa)

        return account_logs

    def consulta_fornecedor_pos_insert(self):
        # Destino
        self.__cursor.execute(SQLs.query_consulta_pos_insert_fornecedor)
        suppliers = self.__cursor.fetchall()

        return suppliers

    def consulta_produto_comparacao(self):
        # Destino
        self.__cursor.execute(SQLs.query_consulta_comparacao_produto)
        products = self.__cursor.fetchall()

        return products

    def consulta_pos_insert(self, produto):
        # Destino

        if produto['tabela'] == 'produto':
            self.__cursor.execute(SQLs.query_consulta_pos_insert_produto)
            consulta_pos_insert = self.__cursor.fetchall()

        elif produto['tabela'] == 'fabricante':
            self.__cursor.execute(SQLs.query_consulta_pos_insert_fabricante)
            consulta_pos_insert = self.__cursor.fetchall()

        else:
            self.__cursor.execute(SQLs.query_consulta_pos_insert_principio)
            consulta_pos_insert = self.__cursor.fetchall()

        return consulta_pos_insert

    def insert_pagar(self, bills):
        # Destino

        bill_logs = []
        for bill in bills:
            data = {'first_column': 'nota_fiscal',
                    'first_value': bill['nota_fiscal'],
                    'second_column': 'valor',
                    'second_value': bill['valor']}

            try:
                self.__cursor.execute(SQLs.query_insert_pagar, bill)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                bill_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                bill_logs.append(log)
                continue

        return bill_logs

    def select_receber(self, clientes_selecionados):
        # Origem

        self.__cursor.execute(SQLs.query_select_receber, (clientes_selecionados,))
        receber = self.__cursor.fetchall()

        return receber

    def select_pagar(self, fornecedores_selecionados):
        # Origem

        self.__cursor.execute(SQLs.query_select_pagar, (fornecedores_selecionados,))
        pagar = self.__cursor.fetchall()

        return pagar

    def select_grupo_origem_sapagado(self):
        # Origem

        self.__cursor.execute(SQLs.query_select_grporigem_sapagado)
        grupo = self.__cursor.fetchall()

        return grupo

    def select_grupo_origem_capagado(self):
        # Origem

        self.__cursor.execute(SQLs.query_select_grporigem_capagado)
        grupo = self.__cursor.fetchall()

        return grupo

    def select_grupo_destino_sapagado(self):
        # Destino

        self.__cursor.execute(SQLs.query_select_grpdestino_sapagado)
        grupo = self.__cursor.fetchall()

        return grupo

    def select_grupo_destino_capagado(self):
        # Destino

        self.__cursor.execute(SQLs.query_select_grpdestino_capagado)
        grupo = self.__cursor.fetchall()

        return grupo

    def select_listagem_empresa(self):
        # Origem

        self.__cursor.execute(SQLs.query_select_listagem_empresa)
        empresa = self.__cursor.fetchall()

        return empresa

    def select_listagem_fornecedor(self):
        # Origem

        self.__cursor.execute(SQLs.query_select_listagem_fornecedor)
        fornecedor = self.__cursor.fetchall()

        return fornecedor

    def limpa_campo_auxiliar(self, marcador_limpeza):
        # Destino

        if marcador_limpeza['fabricante'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_fabricante)

        if marcador_limpeza['principio_ativo'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_principio_ativo)

        if marcador_limpeza['produto'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_produto)

        if marcador_limpeza['barras'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_barras)

        if marcador_limpeza['estoque'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_estoque)

        if marcador_limpeza['lote'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_lote)

        if marcador_limpeza['preco_filial'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_preco_filial)

        if marcador_limpeza['fornecedor'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_fornecedor)

        if marcador_limpeza['pagar'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_pagar)

        if marcador_limpeza['empresa'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_empresa)

        if marcador_limpeza['cliente'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_cliente)
            self.__cursor.execute(SQLs.query_update_limpeza_cliente2)

        if marcador_limpeza['receber'] == 'sim':
            self.__cursor.execute(SQLs.query_update_limpeza_receber)
