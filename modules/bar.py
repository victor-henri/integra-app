class Bar:

    def __init__(self, erased, communicator, origin_bars, products_id, products_found, products_after_insert):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_bars = origin_bars
        self.__products_id = products_id
        self.__products_found = products_found
        self.__products_after_insert = products_after_insert
        self.__selected_bars = []

    def start_bars(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__extract_selected_bars()
        self.__bars_treatment()

    def __remove_erased(self):

        for bars in self.__origin_bars:
            if bars['apagado'] == 'S':
                self.__origin_bars.remove(bars)
            else:
                continue

    def __extract_selected_bars(self):

        for bars in self.__origin_bars:
            product_id = int(bars['id_produto'])

            if product_id in self.__products_id:
                self.__selected_bars.append(bars)
            else:
                continue

    def __bars_treatment(self):

        for bars in self.__selected_bars:
            old_id = int(bars['id_produto'])
            id_found = self.__return_new_id(old_id)

            if id_found is None:
                new_id = self.__return_id_after_insert(old_id)
                bars.update({'id_produto_ant': old_id})
                bars.update({'id_produto': new_id})
            else:
                bars.update({'id_produto_ant': bars['id_produto']})
                bars.update({'id_produto': id_found})

            bars['comunicador'] = self.__communicator

    def __return_new_id(self, old_id):

        for product in self.__products_found:
            product_id = int(product['id_produto'])
            new_id = int(product['novo_id'])

            if old_id == product_id:
                return new_id
            else:
                continue

    def __return_id_after_insert(self, product_id):

        for product in self.__products_after_insert:
            old_id = int(product['campo_auxiliar'])
            new_id = int(product['id_produto'])

            if product_id == old_id:
                return new_id
            else:
                continue

    def get_bars(self):
        return self.__selected_bars
