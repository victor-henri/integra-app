from abc import ABC, abstractmethod
from typing import TypedDict


class AccessDatabase(TypedDict):
    host: str
    user: str
    password: str
    database: str
    port: int

class RepositoryInterface(ABC):

    @abstractmethod
    def create_cursor(self) -> None:
        pass

    @abstractmethod
    def __unicode_error(self, data: dict, error: UnicodeEncodeError) -> dict:
        pass

    @abstractmethod
    def __exception_error(self, data: dict, error: Exception) -> dict:
        pass

    # SELECTS

    @abstractmethod
    def select_manufacturer(self) -> list[dict]:
        pass

    @abstractmethod
    def select_principle(self) -> list[dict]:
        pass

    @abstractmethod
    def select_group_filtered(self) -> list[dict]:
        pass

    @abstractmethod
    def select_group_not_filtered(self) -> list[dict]:
        pass

    @abstractmethod
    def select_product(self) -> list[dict]:
        pass

    @abstractmethod
    def select_stock(self) -> list[dict]:
        pass

    @abstractmethod
    def select_partition(self) -> list[dict]:
        pass

    @abstractmethod
    def select_price(self) -> list[dict]:
        pass

    @abstractmethod
    def select_bar(self) -> list[dict]:
        pass

    @abstractmethod
    def select_company(self, selected_companies) -> list[dict]:
        pass

    @abstractmethod
    def select_customer(self, selected_companies) -> list[dict]:
        pass

    @abstractmethod
    def select_account(self, selected_customers) -> list[dict]:
        pass

    @abstractmethod
    def select_origin_supplier(self, selected_suppliers) -> list[dict]:
        pass

    @abstractmethod
    def select_destiny_supplier(self) -> list[dict]:
        pass

    @abstractmethod
    def select_bill(self, selected_suppliers) -> list[dict]:
        pass

    @abstractmethod
    def select_get_products(self) -> list[dict]:
        pass

    @abstractmethod
    def select_product_comparison(self) -> list[dict]:
        pass

    @abstractmethod
    def select_listing_company(self) -> list[dict]:
        pass

    @abstractmethod
    def select_listing_supplier(self) -> list[dict]:
        pass

    @abstractmethod
    def select_supplier_after_insert(self) -> list[dict]:
        pass

    @abstractmethod
    def query_tables(self, table_data) -> list[dict]:
        pass

    # INSERTS

    @abstractmethod
    def insert_manufacturer(self, manufacturers) -> list[dict]:
        pass

    @abstractmethod
    def insert_principle(self, principles) -> list[dict]:
        pass

    @abstractmethod
    def insert_product(self, products) -> list[dict]:
        pass

    @abstractmethod
    def insert_stock(self, stocks) -> list[dict]:
        pass

    @abstractmethod
    def insert_partition(self, partitions) -> list[dict]:
        pass

    @abstractmethod
    def insert_price(self, prices) -> list[dict]:
        pass

    @abstractmethod
    def insert_bar(self, bars) -> list[dict]:
        pass

    @abstractmethod
    def insert_company(self, companies) -> list[dict]:
        pass

    @abstractmethod
    def insert_customer(self, customers) -> list[dict]:
        pass

    @abstractmethod
    def insert_account(self, accounts) -> list[dict]:
        pass

    @abstractmethod
    def insert_supplier(self, suppliers) -> list[dict]:
        pass

    @abstractmethod
    def insert_bill(self, bills) -> list[dict]:
        pass

    @abstractmethod
    def update_product(self, data_update) -> None:
        pass

    @abstractmethod
    def data_cleaning(self, cleaning_marker) -> None:
        pass
