from typing import TypedDict
from mariadb.mariadb_connection import ConnectionMariaDb
from mariadb.mariadb_repository import RepositoryMariaDb
from modules.manufacturer import Manufacturer
from modules.principle import Principle
from modules.product import Product
from modules.bar import Bar
from modules.stock import Stock
from modules.partition import Partition
from modules.price import Price
from modules.supplier import Supplier
from modules.bill import Bill
from modules.company import Company
from modules.customer import Customer
from modules.account import Account


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

    def start_process(self, erased, communicator, module_marker, selected_groups, selected_suppliers, selected_companies, product_options, manufacturer_id, principle_id, origin_branch_id, destiny_branch_id):

        product_table = {'tabela': 'produto'}
        manufacturer_table = {'tabela': 'fabricante'}
        principle_table = {'tabela': 'principio_ativo'}

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
        if module_marker['estoque'] == 'sim':

            origin_stock = self.__origin_repository.select_stock()

            stock = Stock(erased=erased,
                          communicator=communicator,
                          products_id=products_id,
                          products_found= products_found,
                          products_after_insert = products_after_insert,
                          origin_stock=origin_stock,
                          origin_branch_id=origin_branch_id, 
                          destiny_branch_id=destiny_branch_id)

            stock.start_stock()
            selected_stock = stock.get_stock()
            self.__stock_log = self.__destiny_repository.insert_stock(selected_stock)

        # PARTITION
        if module_marker['lote'] == 'sim':

            origin_partition = self.__origin_repository.select_partition()

            partition = Partition(erased=erased,
                                  communicator=communicator,
                                  products_id=products_id,
                                  products_found=products_found,
                                  products_after_insert=products_after_insert,
                                  origin_partition=origin_partition,
                                  origin_branch_id=origin_branch_id,
                                  destiny_branch_id=destiny_branch_id)

            partition.start_partition()
            selected_partition = partition.get_partition()
            self.__partition_log = self.__destiny_repository.insert_partition(selected_partition)

        # PRICE
        if module_marker['preco'] == 'sim':

            origin_price = self.__origin_repository.select_price()

            price = Price(erased=erased,
                          communicator=communicator,
                          products_id=products_id,
                          products_found=products_found,
                          products_after_insert=products_after_insert,
                          origin_price=origin_price,
                          origin_branch_id=origin_branch_id,
                          destiny_branch_id=destiny_branch_id)

            price.start_price()
            selected_price = price.get_price()
            self.__price_log = self.__destiny_repository.insert_price(selected_price)


        # SUPPLIER
        if module_marker['fornecedor'] == 'sim':
            selected_suppliers = self.get_suppliers()
            origin_suppliers = self.__origin_repository.select_origin_supplier(selected_suppliers)
            destiny_suppliers = self.__destiny_repository.select_destiny_supplier()

            supplier = Supplier(erased=erased,
                                communicator=communicator,
                                origin_suppliers=origin_suppliers,
                                destiny_suppliers=destiny_suppliers)

            supplier.start_supplier()
            suppliers_found = supplier.get_suppliers_found()
            suppliers_not_found = supplier.get_suppliers_not_found()
            self.__supplier_log = self.__destiny_repository.insert_supplier(suppliers_not_found)
            suppliers_after_insert = self.__destiny_repository.select_supplier_after_insert()

        # BILLS TO PAY
        if module_marker['pagar'] == 'sim':

            origin_bills = self.__destiny_repository.select_bill(selected_suppliers)

            bills = Bill(erased=erased,
                         communicator=communicator,
                         origin_bills=origin_bills,
                         origin_branch_id=origin_branch_id,
                         destiny_branch_id=destiny_branch_id,
                         suppliers_found=suppliers_found,
                         suppliers_after_insert=suppliers_after_insert)

            bills.start_bill()
            selected_bill = bills.get_bills()
            self._bill_log = self.__destiny_repository.insert_bill(selected_bill)

        # COMPANY/CUSTOMERS
        if module_marker['empresa'] == 'sim':

            origin_companies = self.__destiny_repository.select_company(selected_companies)

            company = Company(erased=erased,
                              communicator=communicator,
                              origin_companies=origin_companies)

            company.start_company()
            companies = company.get_companies()
            self.__company_log = self.__destiny_repository.insert_company(companies)

            origin_customers = self.__destiny_repository.select_customer(selected_companies)

            customer = Customer(erased=erased,
                                communicator=communicator,
                                origin_customers=origin_customers)

            customer.start_customer()
            customers = customer.get_customers()
            self.__customer_log = self.__destiny_repository.insert_customer(customers)
            selected_customers_id = customer.get_customers_id()

        # ACCOUNTS RECEIVABLE
        if module_marker['receber'] == 'sim':

            origin_accounts = self.__destiny_repository.select_account(selected_customers_id)

            account = Account(erased=erased,
                               communicator=communicator,
                               origin_branch_id=origin_branch_id,
                               destiny_branch_id=destiny_branch_id,
                               origin_accounts=origin_accounts)

            account.start_account()
            accounts = account.get_accounts()
            self.__account_log = self.__destiny_repository.insert_account(accounts)

        # LOGS
        self.__logs.update({'manufacturer_logs': self.__manufacturer_log,
                            'principle_logs': self.__principle_log})

        iterator = IteratorSql()
        iterator.connect_destiny(self.db_destiny)
        iterator.limpa_campo_auxiliar(data_cleaning)
