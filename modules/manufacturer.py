class Manufacturer:

    def __init__(self, erased, communicator, origin_manufacturers, destiny_manufacturers):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_manufacturers = origin_manufacturers
        self.__destiny_manufacturers = destiny_manufacturers
        self.__manufacturers_found = []
        self.__manufacturers_not_found = []

    def start_manufacturer(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__search_manufacturers()
        self.__manufacturers_treatment()

    def __remove_erased(self):

        for manufacturer in self.__origin_manufacturers:
            if manufacturer['apagado'] == 'S':
                self.__origin_manufacturers.remove(manufacturer)
            else:
                continue

    def __search_manufacturers(self):

        for manufacturer in self.__origin_manufacturers:
            new_id = self.__return_manufacturer(manufacturer['cnpj'])

            if new_id:
                manufacturer.update({'novo_id': new_id})
                self.__manufacturers_found.append(manufacturer)
            else:
                manufacturer.update({'novo_id': None})
                self.__manufacturers_not_found.append(manufacturer)

    def __return_manufacturer(self, origin_cnpj):

        for manufacturer in self.__destiny_manufacturers:
            destiny_cnpj = manufacturer['cnpj']
            manufacturer_id = int(manufacturer['id_fabricante'])

            if origin_cnpj == destiny_cnpj:
                return manufacturer_id
            else:
                continue

    def __manufacturers_treatment(self):

        for manufacturer in self.__manufacturers_not_found:
            manufacturer.update({'comunicador': self.__communicator})

    def get_manufacturers_found(self):
        return self.__manufacturers_found

    def get_manufacturers_not_found(self):
        return self.__manufacturers_not_found
