class Price:

    def __init__(self,
                 erased,
                 communicator,
                 products_id,
                 products_found,
                 products_after_insert,
                 origin_price,
                 origin_branch_id,
                 destiny_branch_id):

        self.__erased = erased
        self.__communicator = communicator
        self.__products_id = products_id
        self.__products_found = products_found
        self.__products_after_insert = products_after_insert
        self.__origin_price = origin_price
        self.__origin_branch_id = origin_branch_id
        self.__destiny_branch_id = destiny_branch_id
        self.__selected_prices = []

    def start_price(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__extract_selected_data()
        self.__price_treatment()

    def __remove_erased(self):

        for price in self.__origin_price:
            if price['apagado'] == 'S':
                self.__origin_price.remove(price)
            else:
                continue

    def __extract_selected_data(self):

        for price in self.__origin_price:
            product_id = int(price['id_produto'])
            price_branch_id = int(price['id_filial'])

            if product_id in self.__products_id and price_branch_id == self.__origin_branch_id:
                self.__selected_prices.append(price)
            else:
                continue

    def __price_treatment(self):

        for price in self.__selected_prices[:]:
            old_id = int(price['id_produto'])
            id_found = self.__return_new_id(old_id)

            if id_found is None:
                new_id = self.__return_id_after_insert(old_id)
                price.update({'id_produto_ant': old_id})
                price.update({'id_produto': new_id})
            else:
                self.__selected_prices.remove(price)

            dates = {'inicio': price['inicio_promocao'],
                     'final': price['final_promocao']}

            treated_dates = self.__dates_treatment(dates)

            price.update({'inicio_promocao': treated_dates['inicio']})
            price.update({'final_promocao': treated_dates['final']})
            price.update({'id_filial': self.__destiny_branch_id})
            price.update({'comunicador': self.__communicator})

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

    def __dates_treatment(self, dates):

        for key, date in dates.items():
            if date is None:
                pass
            else:
                formatted_date = date.strftime('%Y-%m-%d')
                dates.update({key: formatted_date})

        return dates

    def get_price(self):
        return self.__selected_prices
