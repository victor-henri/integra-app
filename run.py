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


class Run():

    def __init__(self):
        self.__origin_connection = None
        self.__origin_repository = None
        self.__destiny_connection = None
        self.__destiny_repository = None
        self.__logs = {}

    def connect_origin(self, access_data: dict) -> dict:

        connection = ConnectionMariaDb()
        log = connection.connect_database(access_data)
        self.__origin_connection = connection.get_connection()
        self.__create_origin_repository()

        return log

    def connect_destiny(self, access_data: dict) -> dict:

        connection = ConnectionMariaDb()
        log = connection.connect_database(access_data)
        self.__destiny_connection = connection.get_connection()
        self.__create_destiny_repository()

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

    def get_log(self):
        return self.__logs

    def __set_log(self, log):
        self.__logs.update(log)

    def start_process(self, **kwargs) -> None:

        product_table = {'tabela': 'produto'}
        manufacturer_table = {'tabela': 'fabricante'}
        principle_table = {'tabela': 'principio_ativo'}

        # MANUFACTURER
        if kwargs['module_marker']['fabricante'] is True:

            origin_manufacturers = self.__origin_repository.select_manufacturer()
            destiny_manufacturers = self.__destiny_repository.select_manufacturer()

            manufacturer = Manufacturer(erased=kwargs['erased'],
                                        communicator=kwargs['communicator'],
                                        origin_manufacturers=origin_manufacturers,
                                        destiny_manufacturers=destiny_manufacturers)

            manufacturer.start_manufacturer()
            manufacturers_found = manufacturer.get_manufacturers_found()
            manufacturers_not_found = manufacturer.get_manufacturers_not_found()
            manufacturer_log = self.__destiny_repository.insert_manufacturer(manufacturers_not_found)
            self.__set_log({'manufacturer_logs': manufacturer_log})

        # PRINCIPLE
        if kwargs['module_marker']['principio_ativo'] is True:

            origin_principles = self.__origin_repository.select_principle()
            destiny_principles = self.__destiny_repository.select_principle()

            principle = Principle(erased=kwargs['erased'],
                                  communicator=kwargs['communicator'],
                                  origin_principles=origin_principles,
                                  destiny_principles=destiny_principles)
           
            principle.start_principle()
            principles_found = principle.get_principles_found()
            principles_not_found = principle.get_principles_not_found()
            principle_log = self.__destiny_repository.insert_principle(principles_not_found)
            self.__set_log({'principle_logs': principle_log})

        # PRODUCT
        if kwargs['module_marker']['produto'] is True:

            origin_products = self.__origin_repository.select_product()
            products_comparison = self.__destiny_repository.select_product_comparison()

            product = Product(erased=kwargs['erased'],
                              communicator=kwargs['communicator'],
                              product_options=kwargs['product_options'],
                              origin_products=origin_products,
                              selected_groups=kwargs['selected_groups'],
                              manufacturers_found=manufacturers_found,
                              manufacturer_id=kwargs['manufacturer_id'],
                              principles_found=principles_found,
                              principle_id=kwargs['principle_id'],
                              products_comparison=products_comparison)

            product.start_product()
            products_not_found = product.get_products()
            product_log = self.__destiny_repository.insert_product(products_not_found)
            self.__set_log({'product_logs': product_log})

            products_after_insert = self.__destiny_repository.query_tables(product_table)
            manufacturers_after_insert = self.__destiny_repository.query_tables(manufacturer_table)
            principles_after_insert = self.__destiny_repository.query_tables(principle_table)

            data_update = product.update_after_insert(products_after_insert,
                                                      manufacturers_after_insert,
                                                      principles_after_insert)
            self.__destiny_repository.update_product(data_update['manufacturer'])
            self.__destiny_repository.update_product(data_update['principle'])

            products_id = product.get_products_id()
            products_found = product.get_products_found()

        # BARS
        if kwargs['module_marker']['barras'] is True:

            origin_bars = self.__origin_repository.select_bar()

            bars = Bar(erased=kwargs['erased'],
                       communicator=kwargs['communicator'],
                       origin_bars=origin_bars,
                       products_id=products_id,
                       products_found=products_found,
                       products_after_insert=products_after_insert)

            bars.start_bars()
            selected_bars = bars.get_bars()
            bar_log = self.__destiny_repository.insert_bar(selected_bars)
            self.__set_log({'bar_logs': bar_log})

        # STOCK
        if kwargs['module_marker']['estoque'] is True:

            origin_stock = self.__origin_repository.select_stock()

            stock = Stock(erased=kwargs['erased'],
                          communicator=kwargs['communicator'],
                          products_id=products_id,
                          products_found= products_found,
                          products_after_insert = products_after_insert,
                          origin_stock=origin_stock,
                          origin_branch_id=kwargs['origin_branch_id'],
                          destiny_branch_id=kwargs['destiny_branch_id'])

            stock.start_stock()
            selected_stock = stock.get_stock()
            stock_log = self.__destiny_repository.insert_stock(selected_stock)
            self.__set_log({'stock_logs': stock_log})

        # PARTITION
        if kwargs['module_marker']['lote'] is True:

            origin_partition = self.__origin_repository.select_partition()

            partition = Partition(erased=kwargs['erased'],
                                  communicator=kwargs['communicator'],
                                  products_id=products_id,
                                  products_found=products_found,
                                  products_after_insert=products_after_insert,
                                  origin_partition=origin_partition,
                                  origin_branch_id=kwargs['origin_branch_id'],
                                  destiny_branch_id=kwargs['destiny_branch_id'])

            partition.start_partition()
            selected_partition = partition.get_partition()
            partition_log = self.__destiny_repository.insert_partition(selected_partition)
            self.__set_log({'partition_logs': partition_log})

        # PRICE
        if kwargs['module_marker']['preco'] is True:

            origin_price = self.__origin_repository.select_price()

            price = Price(erased=kwargs['erased'],
                          communicator=kwargs['communicator'],
                          products_id=products_id,
                          products_found=products_found,
                          products_after_insert=products_after_insert,
                          origin_price=origin_price,
                          origin_branch_id=kwargs['origin_branch_id'],
                          destiny_branch_id=kwargs['destiny_branch_id'])

            price.start_price()
            selected_price = price.get_price()
            price_log = self.__destiny_repository.insert_price(selected_price)
            self.__set_log({'price_logs': price_log})


        # SUPPLIER
        if kwargs['module_marker']['fornecedor'] is True:
            selected_suppliers = self.get_suppliers()
            origin_suppliers = self.__origin_repository.select_origin_supplier(selected_suppliers)
            destiny_suppliers = self.__destiny_repository.select_destiny_supplier()

            supplier = Supplier(erased=kwargs['erased'],
                                communicator=kwargs['communicator'],
                                origin_suppliers=origin_suppliers,
                                destiny_suppliers=destiny_suppliers)

            supplier.start_supplier()
            suppliers_found = supplier.get_suppliers_found()
            suppliers_not_found = supplier.get_suppliers_not_found()
            supplier_log = self.__destiny_repository.insert_supplier(suppliers_not_found)
            self.__set_log({'supplier_logs': supplier_log})

            suppliers_after_insert = self.__destiny_repository.select_supplier_after_insert()

        # BILLS TO PAY
        if kwargs['module_marker']['pagar'] is True:

            origin_bills = self.__destiny_repository.select_bill(selected_suppliers)

            bills = Bill(erased=kwargs['erased'],
                         communicator=kwargs['communicator'],
                         origin_bills=origin_bills,
                         origin_branch_id=kwargs['origin_branch_id'],
                         destiny_branch_id=kwargs['destiny_branch_id'],
                         suppliers_found=suppliers_found,
                         suppliers_after_insert=suppliers_after_insert)

            bills.start_bill()
            selected_bill = bills.get_bills()
            bill_log = self.__destiny_repository.insert_bill(selected_bill)
            self.__set_log({'bill_logs': bill_log})

        # COMPANY/CUSTOMERS
        if kwargs['module_marker']['empresa'] is True:

            origin_companies = self.__destiny_repository.select_company(kwargs['selected_companies'])

            company = Company(erased=kwargs['erased'],
                              communicator=kwargs['communicator'],
                              origin_companies=origin_companies)

            company.start_company()
            companies = company.get_companies()
            company_log = self.__destiny_repository.insert_company(companies)
            self.__set_log({'company_logs': company_log})

            origin_customers = self.__destiny_repository.select_customer(kwargs['selected_companies'])

            customer = Customer(erased=kwargs['erased'],
                                communicator=kwargs['communicator'],
                                origin_customers=origin_customers)

            customer.start_customer()
            customers = customer.get_customers()
            customer_log = self.__destiny_repository.insert_customer(customers)
            self.__set_log({'customer_logs': customer_log})

            selected_customers_id = customer.get_customers_id()

        # ACCOUNTS RECEIVABLE
        if kwargs['module_marker']['receber'] is True:

            origin_accounts = self.__destiny_repository.select_account(selected_customers_id)

            account = Account(erased=kwargs['erased'],
                               communicator=kwargs['communicator'],
                               origin_branch_id=kwargs['origin_branch_id'],
                               destiny_branch_id=kwargs['destiny_branch_id'],
                               origin_accounts=origin_accounts)

            account.start_account()
            accounts = account.get_accounts()
            account_log = self.__destiny_repository.insert_account(accounts)
            self.__set_log({'account_logs': account_log})

        # CLEANING FIELDS
        self.__destiny_repository.data_cleaning()
