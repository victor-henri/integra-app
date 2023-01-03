class Supplier():

    def __init__(self, erased, communicator, origin_suppliers, destiny_suppliers):
        self.__erased = erased
        self.__communicator = communicator
        self.__origin_suppliers = origin_suppliers
        self.__destiny_suppliers = destiny_suppliers
        self.__suppliers_found = []
        self.__suppliers_not_found = []

    def start_supplier(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__search_suppliers()
        self.__suppliers_treatment()

    def __remove_erased(self):

        for supplier in self.__origin_suppliers:
            if supplier['apagado'] == 'S':
                self.__origin_suppliers.remove(supplier)
            else:
                continue

    def __search_suppliers(self):

        for supplier in self.__origin_suppliers:
            new_id = self.__return_supplier(supplier['cnpj'])

            if new_id:
                supplier.update({'novo_id': new_id})
                self.__suppliers_found.append(supplier)
            else:
                supplier.update({'novo_id': None})
                self.__suppliers_not_found.append(supplier)

    def __return_supplier(self, origin_cnpj):

        for supplier in self.__destiny_suppliers:
            destiny_cnpj = supplier['cnpj']
            supplier_id = int(supplier['id_fornecedor'])

            if origin_cnpj == destiny_cnpj:
                return supplier_id
            else:
                continue

    def __suppliers_treatment(self):

        for supplier in self.__suppliers_not_found:
            supplier.update({'comunicador': self.__communicator})

    def get_suppliers_found(self):
        return self.__suppliers_found

    def get_suppliers_not_found(self):
        return self.__suppliers_not_found
