from interfaces.repository import RepositoryInterface
from mariadb.mariadb_connection import ConnectionMariaDb
from typing import Type
import pymysql
import sqls


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

    def select_product(self):
        # Origem
        self.__cursor.execute(sqls.SELECT_PRODUCT)
        product = self.__cursor.fetchall()

        return product

    def insert_product(self, products):
        # Destino

        product_logs = []
        for product in products:
            data = {'first_column': 'id_produto',
                    'first_value': product['id_produto'],
                    'second_column': 'descricao',
                    'second_value': product['descricao']}

            if product['novo_id'] is None:
                try:
                    self.__cursor.execute(sqls.INSERT_PRODUCT, product)

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

    def query_tables(self, table_data):
        # Destino
        # consulta_produto_pos_insert

        if table_data['tabela'] == 'produto':
            self.__cursor.execute('SELECT id_produto, campo_auxiliar '
                                   'FROM produto '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            data_after_insert = self.__cursor.fetchall()

        elif table_data['tabela'] == 'fabricante':
            self.__cursor.execute('SELECT id_fabricante, campos_auxiliar '
                                   'FROM fabricante '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            data_after_insert = self.__cursor.fetchall()

        elif table_data['tabela'] == 'principio_ativo':
            self.__cursor.execute('SELECT id_principio_ativo, campo_auxiliar '
                                   'FROM principio_ativo '
                                   'WHERE campo_auxiliar IS NOT NULL;')
            data_after_insert = self.__cursor.fetchall()

        return data_after_insert

    def consulta_pos_insert(self, produto):
        # Destino
        # Verificar este metodo

        if produto['tabela'] == 'produto':
            self.__cursor.execute(sqls.SELECT_PRODUCT_AFTER_INSERT)
            consulta_pos_insert = self.__cursor.fetchall()

        elif produto['tabela'] == 'fabricante':
            self.__cursor.execute(sqls.SELECT_MANUFACTURER_AFTER_INSERT)
            consulta_pos_insert = self.__cursor.fetchall()

        else:
            self.__cursor.execute(sqls.SELECT_PRINCIPLE_AFTER_INSERT)
            consulta_pos_insert = self.__cursor.fetchall()

        return consulta_pos_insert

    def update_product(self, data_update):
        # Destino
        # atualiza_campo_produto_pos_insert

        if data_update['campo'] == 'fabricante':
            self.__cursor.execute('UPDATE produto '
                                   'SET id_fabricante = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', data_update)

        else:
            self.__cursor.execute('UPDATE produto '
                                   'SET id_principio_ativo = %(valor)s '
                                   'WHERE id_produto = %(id_produto)s;', data_update)

    def select_manufacturer(self):
        # Origem
        self.__cursor.execute(sqls.SELECT_MANUFACTURER)
        manufacturer = self.__cursor.fetchall()

        return manufacturer

    # def select_fabricante_destino(self):
    #     # Destino
    #     # Remover este método

    #     self.__cursor.execute(sqls.query_select_fabricante)
    #     manufacturer = self.__cursor.fetchall()

    #     return manufacturer

    def insert_manufacturer(self, manufacturers):
        # Destino

        manufacturer_logs = []
        for manufacturer in manufacturers:
            data = {'first_column': 'id_fabricante',
                    'first_value': manufacturer['id_fabricante'],
                    'second_column': 'descricao',
                    'second_value': manufacturer['descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_MANUFACTURER, manufacturer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                manufacturer_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                manufacturer_logs.append(log)
                continue

        return manufacturer_logs

    def select_principle(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_PRINCIPLE)
        principle = self.__cursor.fetchall()

        return principle

    # def select_principio_ativo_destino(self):
    #     # Destino
    #     # Remover este metodo

    #     self.__cursor.execute(sqls.query_select_principio)
    #     principio_ativo = self.__cursor.fetchall()

    #     return principio_ativo

    def insert_principle(self, principles):
        # Destino

        principle_logs = []
        for principle in principles:
            data = {'first_column': 'id_principio_ativo',
                    'first_value': principle['id_principio_ativo'],
                    'second_column': 'descricao',
                    'second_value': principle['descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_PRINCIPLE, principle)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                principle_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                principle_logs.append(log)
                continue

        return principle_logs

    def select_bar(self):
        # Origem
        self.__cursor.execute(sqls.SELECT_BAR)
        bars = self.__cursor.fetchall()

        return bars

    def insert_bar(self, bars):
        # Destino

        bar_logs = []
        for item in bars:
            data = {'first_column': 'id_produto',
                    'first_value': item['id_produto'],
                    'second_column': 'barras',
                    'second_value': item['barras']}

            try:
                self.__cursor.execute(sqls.INSERT_BAR, item)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                bar_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                bar_logs.append(log)
                continue

        return bar_logs

    def select_stock(self):
        # Origem
        self.__cursor.execute(sqls.SELECT_STOCK)
        stock = self.__cursor.fetchall()

        return stock

    def insert_stock(self, stocks):
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
                    self.__cursor.execute(sqls.SELECT_UPDATE_STOCK, stock)
                    estoque_existente = self.__cursor.fetchone()
                    estoque_existente.update({'estoque': estoque_existente['estoque'] + estoque_atual})
                    self.__cursor.execute(sqls.UPDATE_STOCK, estoque_existente)

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
                    self.__cursor.execute(sqls.INSERT_STOCK, stock)

                except UnicodeEncodeError as error:
                    log = self.__unicode_error(data, error)
                    stock_logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    stock_logs.append(log)
                    continue

        return stock_logs

    def select_get_products(self):
        # Destino
        # select_produto_pos_insert

        self.__cursor.execute('SELECT id_produto, campo_auxiliar FROM produto;')
        product = self.__cursor.fetchall()

        return product

    def select_partition(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_PARTITION)
        partition = self.__cursor.fetchall()

        return partition

    def insert_partition(self, partitions):
        # Destino

        partition_logs = []
        for partition in partitions:
            data = {'first_column': 'id_produto',
                    'first_value': partition['id_produto'],
                    'second_column': 'lote_descricao',
                    'second_value': partition['lote_descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_PARTITION, partition)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                partition_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                partition_logs.append(log)
                continue

        return partition_logs

    def select_price(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_PRICE)
        price = self.__cursor.fetchall()

        return price

    def insert_price(self, prices):
        # Destino

        price_logs = []
        for price in prices:
            data = {'first_column': 'id_produto',
                    'first_value': price['id_produto'],
                    'second_column': 'id_produto',
                    'second_value': price['id_produto']}

            try:
                self.__cursor.execute(sqls.INSERT_PRICE, price)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                price_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                price_logs.append(log)
                continue

        return price_logs

    def select_company(self, selected_companies):
        # Origem
        self.__cursor.execute(sqls.SELECT_COMPANY, (selected_companies,))
        company = self.__cursor.fetchall()

        return company

    def select_origin_supplier(self, selected_suppliers):
        # Origem
        self.__cursor.execute(sqls.SELECT_SUPPLIER_ORIGIN, (selected_suppliers,))
        supplier = self.__cursor.fetchall()

        return supplier

    def select_destiny_supplier(self):
        # Destino
        self.__cursor.execute(sqls.SELECT_SUPPLIER_DESTINY)
        supplier = self.__cursor.fetchall()

        return supplier

    def select_customer(self, selected_companies):
        # Origem
        self.__cursor.execute(sqls.SELECT_CUSTOMER, (selected_companies,))
        customer = self.__cursor.fetchall()

        return customer

    def insert_company(self, companies):
        # Destino

        company_logs = []
        for company in companies:
            data = {'first_column': 'id_empresa',
                    'first_value': company['id_empresa'],
                    'second_column': 'nome_fantasia',
                    'second_value': company['nome_fantasia']}

            try:
                self.__cursor.execute(sqls.INSERT_COMPANY, company)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                company_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                company_logs.append(log)
                continue

        return company_logs

    def insert_supplier(self, suppliers):
        # Destino

        supplier_logs = []
        for supplier in suppliers:
            data = {'first_column': 'id_fornecedor',
                    'first_value': supplier['id_fornecedor'],
                    'second_column': 'nome_fantasia',
                    'second_value': supplier['nome_fantasia']}

            try:
                self.__cursor.execute(sqls.INSERT_SUPPLIER, supplier)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                supplier_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                supplier_logs.append(log)
                continue

        return supplier_logs

    def insert_customer(self, customers):
        # Destino

        customer_logs = []
        for customer in customers:
            data = {'first_column': 'id_cliente',
                    'first_value': customer['id_cliente'],
                    'second_column': 'nome',
                    'second_value': customer['nome']}

            try:
                self.__cursor.execute(sqls.INSERT_CUSTOMER, customer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                customer_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                customer_logs.append(log)
                continue

        # Atualiza o id_empresa da tabela cliente com os novos ids de empresas inseridas
        self.__cursor.execute(sqls.UPDATE_CUSTOMER)

        return customer_logs

    def insert_account(self, accounts):
        # Destino

        account_logs = []
        for account in accounts:
            data = {'first_column': 'id_cliente',
                    'first_value': account['id_cliente'],
                    'second_column': 'valor',
                    'second_value': account['valor']}

            try:
                self.__cursor.execute(sqls.INSERT_ACCOUNT, account)

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
        self.__cursor.execute(sqls.UPDATE_CUSTOMER_ACCOUNT)

        # Atualiza o id_empresa da tabela receber com os novos ids de empresas.
        self.__cursor.execute(sqls.UPDATE_COMPANY_ACCOUNT)

        return account_logs

    def select_supplier_after_insert(self):
        # Destino
        # consulta_fornecedor_pos_insert

        self.__cursor.execute(sqls.SELECT_SUPPLIER_AFTER_INSERT)
        suppliers = self.__cursor.fetchall()

        return suppliers

    def select_product_comparison(self):
        # Destino
        # consulta_produto_comparacao

        self.__cursor.execute(sqls.SELECT_PRODUCT_COMPARISON)
        products = self.__cursor.fetchall()

        return products

    def insert_bill(self, bills):
        # Destino

        bill_logs = []
        for bill in bills:
            data = {'first_column': 'nota_fiscal',
                    'first_value': bill['nota_fiscal'],
                    'second_column': 'valor',
                    'second_value': bill['valor']}

            try:
                self.__cursor.execute(sqls.INSERT_BILL, bill)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                bill_logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                bill_logs.append(log)
                continue

        return bill_logs

    def select_account(self, selected_customers):
        # Origem

        self.__cursor.execute(sqls.SELECT_ACCOUNT, (selected_customers,))
        account = self.__cursor.fetchall()

        return account

    def select_bill(self, selected_suppliers):
        # Origem

        self.__cursor.execute(sqls.SELECT_BILL, (selected_suppliers,))
        bill = self.__cursor.fetchall()

        return bill

    def select_origin_group_nerased(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_ORIGIN_GROUP_NERASED)
        group = self.__cursor.fetchall()

        return group

    def select_origin_group_erased(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_ORIGIN_GROUP_ERASED)
        group = self.__cursor.fetchall()

        return group

    def select_group_destiny_nerased(self):
        # Destino

        self.__cursor.execute(sqls.SELECT_GROUP_DESTINY_NERASED)
        group = self.__cursor.fetchall()

        return group

    def select_group_destiny_erased(self):
        # Destino

        self.__cursor.execute(sqls.SELECT_GROUP_DESTINY_ERASED)
        group = self.__cursor.fetchall()

        return group

    def select_listing_company(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_LISTING_COMPANY)
        company = self.__cursor.fetchall()

        return company

    def select_listing_supplier(self):
        # Origem

        self.__cursor.execute(sqls.SELECT_LISTING_SUPPLIER)
        supplier = self.__cursor.fetchall()

        return supplier

    def data_cleaning(self, cleaning_marker):
        # Destino

        if cleaning_marker['fabricante'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_MANUFACTURER)

        if cleaning_marker['principio_ativo'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_PRINCIPLE)

        if cleaning_marker['produto'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_PRODUCT)

        if cleaning_marker['barras'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_BARS)

        if cleaning_marker['estoque'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_STOCK)

        if cleaning_marker['lote'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_PARTITION)

        if cleaning_marker['preco_filial'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_PRICE)

        if cleaning_marker['fornecedor'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_SUPPLIER)

        if cleaning_marker['pagar'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_BILL)

        if cleaning_marker['empresa'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_COMPANY)

        if cleaning_marker['cliente'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_CUSTOMER)
            self.__cursor.execute(sqls.UPDATE_CLEANING_CUSTOMER2)

        if cleaning_marker['receber'] == 'sim':
            self.__cursor.execute(sqls.UPDATE_CLEANING_ACCOUNT)
