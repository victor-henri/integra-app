from typing import Type
from interfaces.repository import RepositoryInterface
from mariadb.mariadb_connection import ConnectionInterface
import sqls


class RepositoryMariaDb(RepositoryInterface):
    """_summary_

    Args:
        RepositoryInterface (_type_): _description_
    """

    def __init__(self, connection: Type[ConnectionInterface]):
        self.__connection = connection
        self.__cursor = None

    def create_cursor(self) -> None:
        """Creates a cursor with the connection object.
        """
        self.__cursor = self.__connection.cursor()

    def __unicode_error(self, data: dict, error: UnicodeEncodeError) -> dict:
        error_register = f"{data['first_column']}: {data['first_value']}" \
                            f" | {data['second_column']}: {data['second_value']} não importado."
        error_return = f"Erro na codificação de caracteres - Descrição: {error}"
        log = {'error_register': error_register, 'error_return': error_return}

        return log

    def __exception_error(self, data: dict, error: Exception) -> dict:
        error_register = f"{data['first_column']}: {data['first_value']}" \
                         f" | {data['second_column']}: {data['second_value']} não importado."
        error_return = f"Descrição: {error}"
        log = {'error_register': error_register, 'error_return': error_return}

        return log

    # SELECTS

    def select_manufacturer(self) -> list[dict]:

        self.__cursor.execute(sqls.SELECT_MANUFACTURER)
        manufacturer = self.__cursor.fetchall()

        return manufacturer

    def select_principle(self) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_PRINCIPLE)
        principle = self.__cursor.fetchall()

        return principle

    def select_group_filtered(self) -> list[dict]:
        self.__cursor.execute(sqls.SELECT_GROUP_FILTERED)
        group = self.__cursor.fetchall()

        return group

    def select_group_not_filtered(self) -> list[dict]:
        self.__cursor.execute(sqls.SELECT_GROUP_NOT_FILTERED)
        group = self.__cursor.fetchall()

        return group

    def select_product(self) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_PRODUCT)
        product = self.__cursor.fetchall()

        return product

    def select_stock(self) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_STOCK)
        stock = self.__cursor.fetchall()

        return stock

    def select_partition(self) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_PARTITION)
        partition = self.__cursor.fetchall()

        return partition

    def select_price(self) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_PRICE)
        price = self.__cursor.fetchall()

        return price

    def select_bar(self) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_BAR)
        bars = self.__cursor.fetchall()

        return bars

    def select_company(self, selected_companies) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_COMPANY, (selected_companies,))
        company = self.__cursor.fetchall()

        return company

    def select_customer(self, selected_companies) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_CUSTOMER, (selected_companies,))
        customer = self.__cursor.fetchall()

        return customer

    def select_account(self, selected_customers) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_ACCOUNT, (selected_customers,))
        account = self.__cursor.fetchall()

        return account

    def select_origin_supplier(self, selected_suppliers) -> list[dict]:
        # Origem
        self.__cursor.execute(sqls.SELECT_SUPPLIER_ORIGIN, (selected_suppliers,))
        supplier = self.__cursor.fetchall()

        return supplier

    def select_destiny_supplier(self) -> list[dict]:
        # Destino
        self.__cursor.execute(sqls.SELECT_SUPPLIER_DESTINY)
        supplier = self.__cursor.fetchall()

        return supplier

    def select_bill(self, selected_suppliers) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_BILL, (selected_suppliers,))
        bill = self.__cursor.fetchall()

        return bill

    def select_get_products(self) -> list[dict]:
        # Destino
        # select_produto_pos_insert

        self.__cursor.execute('SELECT id_produto, campo_auxiliar FROM produto;')
        product = self.__cursor.fetchall()

        return product

    def select_product_comparison(self) -> list[dict]:
        # Destino
        # consulta_produto_comparacao

        self.__cursor.execute(sqls.SELECT_PRODUCT_COMPARISON)
        products = self.__cursor.fetchall()

        return products

    def select_listing_company(self) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_LISTING_COMPANY)
        company = self.__cursor.fetchall()

        return company

    def select_listing_supplier(self) -> list[dict]:
        # Origem

        self.__cursor.execute(sqls.SELECT_LISTING_SUPPLIER)
        supplier = self.__cursor.fetchall()

        return supplier

    def select_supplier_after_insert(self) -> list[dict]:
        # Destino
        # consulta_fornecedor_pos_insert

        self.__cursor.execute(sqls.SELECT_SUPPLIER_AFTER_INSERT)
        suppliers = self.__cursor.fetchall()

        return suppliers

    def query_tables(self, table_data) -> list[dict]:
        # Destino
        # consulta_produto_pos_insert

        if table_data['tabela'] == 'produto':
            self.__cursor.execute(sqls.SELECT_PRODUCT_AFTER_INSERT)
            data_after_insert = self.__cursor.fetchall()

        elif table_data['tabela'] == 'fabricante':
            self.__cursor.execute(sqls.SELECT_MANUFACTURER_AFTER_INSERT)
            data_after_insert = self.__cursor.fetchall()

        else:
            self.__cursor.execute(sqls.SELECT_PRINCIPLE_AFTER_INSERT)
            data_after_insert = self.__cursor.fetchall()

        return data_after_insert

    # INSERTS

    def insert_manufacturer(self, manufacturers) -> list[dict]:

        logs: list[dict] = []

        for manufacturer in manufacturers:
            data = {'first_column': 'id_fabricante',
                    'first_value': manufacturer['id_fabricante'],
                    'second_column': 'descricao',
                    'second_value': manufacturer['descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_MANUFACTURER, manufacturer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_principle(self, principles) -> list[dict]:

        logs: list[dict] = []

        for principle in principles:
            data = {'first_column': 'id_principio_ativo',
                    'first_value': principle['id_principio_ativo'],
                    'second_column': 'descricao',
                    'second_value': principle['descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_PRINCIPLE, principle)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_product(self, products) -> list[dict]:

        logs: list[dict] = []

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
                    logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    logs.append(log)
                    continue
            else:
                continue

        return logs

    def insert_stock(self, stocks) -> list[dict]:

        logs: list[dict] = []

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
                    logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    logs.append(log)
                    continue

            else:
                try:
                    self.__cursor.execute(sqls.INSERT_STOCK, stock)

                except UnicodeEncodeError as error:
                    log = self.__unicode_error(data, error)
                    logs.append(log)
                    continue

                except Exception as error:
                    log = self.__exception_error(data, error)
                    logs.append(log)
                    continue

        return logs

    def insert_partition(self, partitions) -> list[dict]:

        logs: list[dict] = []

        for partition in partitions:
            data = {'first_column': 'id_produto',
                    'first_value': partition['id_produto'],
                    'second_column': 'lote_descricao',
                    'second_value': partition['lote_descricao']}

            try:
                self.__cursor.execute(sqls.INSERT_PARTITION, partition)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_price(self, prices) -> list[dict]:

        logs: list[dict] = []

        for price in prices:
            data = {'first_column': 'id_produto',
                    'first_value': price['id_produto'],
                    'second_column': 'id_produto',
                    'second_value': price['id_produto']}

            try:
                self.__cursor.execute(sqls.INSERT_PRICE, price)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_bar(self, bars) -> list[dict]:

        logs: list[dict] = []

        for item in bars:
            data = {'first_column': 'id_produto',
                    'first_value': item['id_produto'],
                    'second_column': 'barras',
                    'second_value': item['barras']}

            try:
                self.__cursor.execute(sqls.INSERT_BAR, item)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_company(self, companies) -> list[dict]:

        logs: list[dict] = []

        for company in companies:
            data = {'first_column': 'id_empresa',
                    'first_value': company['id_empresa'],
                    'second_column': 'nome_fantasia',
                    'second_value': company['nome_fantasia']}

            try:
                self.__cursor.execute(sqls.INSERT_COMPANY, company)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_customer(self, customers) -> list[dict]:

        logs: list[dict] = []

        for customer in customers:
            data = {'first_column': 'id_cliente',
                    'first_value': customer['id_cliente'],
                    'second_column': 'nome',
                    'second_value': customer['nome']}

            try:
                self.__cursor.execute(sqls.INSERT_CUSTOMER, customer)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        # Atualiza o id_empresa da tabela cliente com os novos ids de empresas inseridas
        self.__cursor.execute(sqls.UPDATE_CUSTOMER)

        return logs

    def insert_account(self, accounts) -> list[dict]:

        logs: list[dict] = []

        for account in accounts:
            data = {'first_column': 'id_cliente',
                    'first_value': account['id_cliente'],
                    'second_column': 'valor',
                    'second_value': account['valor']}

            try:
                self.__cursor.execute(sqls.INSERT_ACCOUNT, account)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        # Atualiza o id_cliente da tabela receber com os novos ids de clientes inseridos a partir do
        # campo campo_auxiliar que recebeu o id_cliente do banco de origem.
        self.__cursor.execute(sqls.UPDATE_CUSTOMER_ACCOUNT)

        # Atualiza o id_empresa da tabela receber com os novos ids de empresas.
        self.__cursor.execute(sqls.UPDATE_COMPANY_ACCOUNT)

        return logs

    def insert_supplier(self, suppliers) -> list[dict]:

        logs: list[dict] = []

        for supplier in suppliers:
            data = {'first_column': 'id_fornecedor',
                    'first_value': supplier['id_fornecedor'],
                    'second_column': 'nome_fantasia',
                    'second_value': supplier['nome_fantasia']}

            try:
                self.__cursor.execute(sqls.INSERT_SUPPLIER, supplier)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def insert_bill(self, bills) -> list[dict]:

        logs: list[dict] = []

        for bill in bills:
            data = {'first_column': 'nota_fiscal',
                    'first_value': bill['nota_fiscal'],
                    'second_column': 'valor',
                    'second_value': bill['valor']}

            try:
                self.__cursor.execute(sqls.INSERT_BILL, bill)

            except UnicodeEncodeError as error:
                log = self.__unicode_error(data, error)
                logs.append(log)
                continue

            except Exception as error:
                log = self.__exception_error(data, error)
                logs.append(log)
                continue

        return logs

    def update_product(self, data_update) -> None:
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

    # def consulta_pos_insert(self, table_data):
    #     # Destino
    #     # consulta_pos_insert
    #     # Metodo duplicado - remover

    #     if table_data['tabela'] == 'produto':
    #         self.__cursor.execute(sqls.SELECT_PRODUCT_AFTER_INSERT)
    #         consulta_pos_insert = self.__cursor.fetchall()

    #     elif table_data['tabela'] == 'fabricante':
    #         self.__cursor.execute(sqls.SELECT_MANUFACTURER_AFTER_INSERT)
    #         consulta_pos_insert = self.__cursor.fetchall()

    #     else:
    #         self.__cursor.execute(sqls.SELECT_PRINCIPLE_AFTER_INSERT)
    #         consulta_pos_insert = self.__cursor.fetchall()

    #     return consulta_pos_insert

    # def select_fabricante_destino(self):
    #     # Destino
    #     # Remover este método

    #     self.__cursor.execute(sqls.query_select_fabricante)
    #     manufacturer = self.__cursor.fetchall()

    #     return manufacturer

    # def select_principio_ativo_destino(self):
    #     # Destino
    #     # Remover este metodo

    #     self.__cursor.execute(sqls.query_select_principio)
    #     principio_ativo = self.__cursor.fetchall()

    #     return principio_ativo

    def data_cleaning(self, cleaning_marker) -> None:
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
