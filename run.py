from typing import TypedDict
from mariadb.mariadb_connection import ConnectionMariaDb
from mariadb.mariadb_repository import RepositoryMariaDb
from modules.manufacturer import Manufacturer


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

    def start_process(self, erased, communicator, module_marker):

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
        if self.sel_principle_desc.get():

            principle = PrincipioAtivo(dados_origem=self.db_origin,
                                       dados_destino=self.db_destiny,
                                       comunicador=communicator)
            principle_log = principle.inicia_principios_ativos(erased)

            principles_found = principle.retorna_principios_tratados()


        # PRODUCT
        if self.sel_product.get():
            selected_groups = self.get_groups()

            product = Produto(dados_origem=self.db_origin,
                              dados_destino=self.db_destiny,
                              comunicador=communicator,
                              fabricantes_encontrados_tratados=manufacturers_found,
                              principios_encontrados_tratados=principles_found,
                              id_fabricante=manufacturer_id,
                              id_principio=principle_id,
                              grupos_selecionados=selected_groups)

            if self.sel_productbar.get():
                product_update.update({'remover_produtos_barras_zerados': 'sim'})

            if self.sel_manufacturer_cnpj.get():
                product_update.update({'fabricante_por_cnpj': 'sim'})

            if self.sel_manufacturer_id.get():
                product_update.update({'fabricante_por_id': 'sim'})

            if self.sel_principle_desc.get():
                product_update.update({'principio_por_desc': 'sim'})

            if self.sel_principle_id.get():
                product_update.update({'principio_por_id': 'sim'})

            product_log = product.inicia_produtos(marcador_produto=product_update, apagado=erased)

            product_ids = product.retorna_produtos_ids()


        # BARS
        if self.sel_bars.get():

            bars = BarrasAdicional(dados_origem=self.db_origin,
                                   dados_destino=self.db_destiny,
                                   comunicador=communicator,
                                   produtos_ids=product_ids)
            bars_log = bars.inicia_barras(erased)


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
        self.__logs.update({'manufacturer_logs': self.__manufacturer_log})

        iterator = IteratorSql()
        iterator.connect_destiny(self.db_destiny)
        iterator.limpa_campo_auxiliar(data_cleaning)
