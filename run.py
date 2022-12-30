from typing import TypedDict
from mariadb.mariadb_connection import ConnectionMariaDb
from mariadb.mariadb_repository import RepositoryMariaDb
from modules.manufacturer import Manufacturer
from modules.principle import Principle
from modules.product import Product
from modules.bar import Bar


class AccessDatabase(TypedDict):
    """Typing class
    """
    host: str
    user: str
    password: str
    database: str
    port: int


class Run():

    def __init__(self):
        self.__origin_connection = None
        self.__origin_repository = None
        self.__destiny_connection = None
        self.__destiny_repository = None
        self.__manufacturer_log = None
        self.__principle_log = None
        self.__logs = None

    def connect_origin(self, access_data: TypedDict[AccessDatabase]) -> dict:

        connection = ConnectionMariaDb()
        self.__origin_connection = connection.get_connection()

        self.__create_origin_repository()
        log = connection.connect_database(access_data)
        return log

    def connect_destiny(self, access_data: TypedDict[AccessDatabase]) -> dict:

        connection = ConnectionMariaDb()
        self.__destiny_connection = connection.get_connection()

        self.__create_destiny_repository()
        log = connection.connect_database(access_data)
        return log

    def __create_origin_repository(self) -> None:

        self.__origin_repository = RepositoryMariaDb(self.__origin_connection)
        self.__origin_repository.create_cursor()

    def __create_destiny_repository(self) -> None:

        self.__destiny_repository = RepositoryMariaDb(self.__destiny_connection)
        self.__destiny_repository.create_cursor()

    def get_groups(self, option: dict) -> list[dict]:

        if option['database'] == 'origin' and option['filtered']:
            groups = self.__origin_repository.select_group_filtered()
            return groups

        elif option['database'] == 'origin' and option['not_filtered']:
            groups = self.__origin_repository.select_group_not_filtered()
            return groups

        elif option['database'] == 'destiny' and option['filtered']:
            groups = self.__destiny_repository.select_group_filtered()
            return groups

        else:
            groups = self.__destiny_repository.select_group_not_filtered()
            return groups

    def get_companies(self):
        companies = self.__origin_repository.select_listing_company()
        return companies

    def get_suppliers(self):
        suppliers = self.__origin_repository.select_listing_supplier()
        return suppliers

    def get_logs(self):
        return self.__logs

    def start_process(self, erased, communicator, module_marker, selected_groups, product_options, manufacturer_id, principle_id):

        # MANUFACTURER
        if module_marker['fabricante'] == 'sim':

            origin_manufacturers = self.__origin_repository.select_manufacturer()
            destiny_manufacturers = self.__destiny_repository.select_manufacturer()

            manufacturer = Manufacturer(erased=erased,
                                        communicator=communicator,
                                        origin_manufacturers=origin_manufacturers,
                                        destiny_manufacturers=destiny_manufacturers)

            manufacturer.start_manufacturers()
            manufacturers_found = manufacturer.get_manufacturers_found()
            manufacturers_not_found = manufacturer.get_manufacturers_not_found()
            self.__manufacturer_log = self.__destiny_repository.insert_manufacturer(manufacturers_not_found)

        # PRINCIPLE
        if module_marker['principio_ativo'] == 'sim':

            origin_principles = self.__origin_repository.select_principle()
            destiny_principles = self.__destiny_repository.select_principle()

            principle = Principle(erased=erased,
                                  communicator=communicator,
                                  origin_principles=origin_principles,
                                  destiny_principles=destiny_principles)
                                  
            principle.start_principles()
            principles_found = principle.get_principles_found()
            principles_not_found = principle.get_principles_not_found()
            self.__principle_log = self.__destiny_repository.insert_principle(principles_not_found)

        # PRODUCT
        if module_marker['produto'] == 'sim':

            product_table = {'tabela': 'produto'}
            manufacturer_table = {'tabela': 'fabricante'}
            principle_table = {'tabela': 'principio_ativo'}

            origin_products = self.__origin_repository.select_product()
            products_comparison = self.__destiny_repository.select_product_comparison()

            product = Product(erased=erased,
                              communicator=communicator,
                              product_options=product_options,
                              origin_products=origin_products,
                              selected_groups=selected_groups,
                              manufacturers_found=manufacturers_found,
                              manufacturer_id=manufacturer_id,
                              principles_found=principles_found,
                              principle_id=principle_id,
                              products_comparison=products_comparison)

            product.start_product()
            products_not_found = product.get_products()
            self.__product_log = self.__destiny_repository.insert_product(products_not_found)

            products_after_insert = self.__destiny_repository.query_tables(product_table)
            manufacturers_after_insert = self.__destiny_repository.query_tables(manufacturer_table)
            principles_after_insert = self.__destiny_repository.query_tables(principle_table)

            data_update = product.update_after_insert(products_after_insert, manufacturers_after_insert, principles_after_insert)
            self.__destiny_repository.update_product(data_update['manufacturer'])
            self.__destiny_repository.update_product(data_update['principle'])
            
            products_id = product.get_products_id()
            products_found = product.get_products_found()

        # BARS
        if module_marker['barras'] == 'sim':

            origin_bars = self.__origin_repository.select_bar()

            bars = Bar(erased=erased,
                       communicator=communicator,
                       origin_bars=origin_bars,
                       products_id=products_id,
                       products_found=products_found,
                       products_after_insert=products_after_insert)

            bars.start_bars()
            selected_bars = bars.get_bars()
            self.__bar_log = self.__destiny_repository.insert_bar(selected_bars)

        # STOCK
        if self.sel_stock.get():

            stock = Estoque(dados_origem=self.db_origin,
                            dados_destino=self.db_destiny,
                            filial_id_origem=origin_branch_id,
                            filial_id_destino=destiny_branch_id,
                            comunicador=communicator,
                            produtos_ids=product_ids)
            stock_log = stock.inicia_estoque(erased)



        # PARTITION
        if self.sel_partition.get():

            partition = Lote(dados_origem=self.db_origin,
                             dados_destino=self.db_destiny,
                             filial_id_origem=origin_branch_id,
                             filial_id_destino=destiny_branch_id,
                             comunicador=communicator,
                             produtos_ids=product_ids)
            partition_log = partition.inicia_lotes(erased)


        # PRICE
        if self.sel_price.get():

            price = PrecoFilial(dados_origem=self.db_origin,
                                dados_destino=self.db_destiny,
                                filial_id_origem=origin_branch_id,
                                filial_id_destino=destiny_branch_id,
                                comunicador=communicator,
                                produtos_ids=product_ids)
            price_log = price.inicia_precos_filial(erased)


        # SUPPLIER
        if self.sel_suppliers.get():
            selected_suppliers = self.get_suppliers()

            supplier = Fornecedor(dados_origem=self.db_origin,
                                  dados_destino=self.db_destiny,
                                  fornecedores_selecionados=selected_suppliers,
                                  comunicador=communicator)
            supplier_log = supplier.inicia_fornecedores(erased)

            suppliers_found = supplier.retorna_fornecedores_tratados()
            suppliers_after_insert = supplier.retorna_fornecedores_pos_insert()


        # BILLS TO PAY
        if self.sel_bills.get():

            bills = Pagar(dados_origem=self.db_origin,
                          dados_destino=self.db_destiny,
                          filial_id_origem=origin_branch_id,
                          filial_id_destino=destiny_branch_id,
                          fornecedores_encontrados=suppliers_found,
                          fornecedores_selecionados=selected_suppliers,
                          fornecedores_pos_insert=suppliers_after_insert,
                          comunicador=communicator)
            bills_log = bills.inicia_pagar(erased)


        # COMPANY/CUSTOMERS
        if self.sel_companies.get():
            selected_companies = self.get_companies()

            company = Empresa(dados_origem=self.db_origin,
                              dados_destino=self.db_destiny,
                              empresas_selecionadas=selected_companies,
                              comunicador=communicator)
            company_log = company.inicia_empresas(erased)



            customer = Cliente(dados_origem=self.db_origin,
                               dados_destino=self.db_destiny,
                               empresas_selecionadas=selected_companies,
                               comunicador=communicator)
            customer_log = customer.inicia_clientes(erased)

            selected_customers = customer.retorna_clientes_ids()


        # ACCOUNTS RECEIVABLE
        if self.sel_accounts_receivable.get():

            accounts = Receber(dados_origem=self.db_origin,
                               dados_destino=self.db_destiny,
                               filial_id_origem=origin_branch_id,
                               filial_id_destino=destiny_branch_id,
                               empresas_selecionadas=selected_companies,
                               clientes_selecionados=selected_customers,
                               comunicador=communicator)
            accounts_log = accounts.inicia_receber(erased)



        # LOGS
        self.__logs.update({'manufacturer_logs': self.__manufacturer_log,
                            'principle_logs': self.__principle_log})

        iterator = IteratorSql()
        iterator.connect_destiny(self.db_destiny)
        iterator.limpa_campo_auxiliar(data_cleaning)
