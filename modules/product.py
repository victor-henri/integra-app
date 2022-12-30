from datetime import datetime


class Product:

    def __init__(self,
                 erased,
                 communicator,
                 product_options,
                 origin_products,
                 selected_groups,
                 manufacturers_found,
                 manufacturer_id,
                 principles_found,
                 principle_id,
                 products_comparison):

        self.__erased = erased
        self.__communicator = communicator
        self.__product_options = product_options
        self.__origin_products = origin_products
        self.__selected_groups = selected_groups
        self.__selected_products = None
        self.__manufacturers_found = manufacturers_found
        self.__manufacturer_id = manufacturer_id
        self.__principles_found = principles_found
        self.__principle_id = principle_id
        self.__products_comparison = products_comparison
        self.__selected_products_id = []
        self.__products_found = []


    def start_product(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__extract_selected_products()

        if self.__product_options['remover_produtos_barras_zerados'] is True:
            zeros = self.__product_options['quantidade_zeros_barras']
            self.__remove_products_zeros_bar(zeros)

        if self.__product_options['fabricante_por_cnpj'] is True:
            self.__update_manufacturers_cnpj()

        if self.__product_options['fabricante_por_id'] is True:
            self.__update_manufacturers_id()

        if self.__product_options['principio_por_desc'] is True:
            self.__update_principles_description()

        if self.__product_options['principio_por_id'] is True:
            self.__update_principles_id()

        self.__product_treatment()
        self.__data_selection()

    def __remove_erased(self):

        for product in self.__origin_products:
            if product['apagado'] == 'S':
                self.__origin_products.remove(product)
            else:
                continue

    def __extract_selected_products(self):

        groups_id_list: list[int] = []

        for group in self.__selected_groups:
            groups_id_list.append(int(group['antigo_id']))

        self.__selected_products: list[dict] = []

        for product in self.__origin_products:
            current_group_id = int(product['id_grupo'])

            if current_group_id in groups_id_list:
                self.__selected_products.append(product)
            else:
                continue

        for product in self.__selected_products:
            current_group_id = int(product['id_grupo'])
            new_id = self.__return_group(current_group_id)
            product.update({'id_grupo': new_id})

    def __return_group(self, current_group_id):

        for group in self.__selected_groups:
            old_group_id = int(group['antigo_id'])
            new_id = int(group['novo_id'])

            if current_group_id == old_group_id:
                return new_id
            else:
                continue

    def __remove_products_zeros_bar(self, zeros):

        for product in self.__selected_products:
            result = self.__count_zeros(product['barras'], zeros)

            if result is True:
                self.__selected_products.remove(product)
            else:
                continue

    def __count_zeros(self, bars, amount_zeros):

        counter: int = 0
        zeros: str = ''

        while counter < amount_zeros:
            zeros += '0'
            counter += 1

        cut_piece: str = bars[:amount_zeros]
        result: bool = zeros in cut_piece
        return result

    def __update_manufacturers_cnpj(self):

        for product in self.__selected_products:

            if product['id_fabricante'] is None:
                product['id_fabricante_ant'] = None
            else:
                current_id = int(product['id_fabricante'])
                new_id = self.__return_manufacturer_new_id(current_id)

                if new_id:
                    product.update({'id_fabricante': new_id, 'id_fabricante_ant': None})
                else:
                    product.update({'id_fabricante_ant': current_id, 'id_fabricante': None})

    def __return_manufacturer_new_id(self, current_id):

        for manufacturer in self.__manufacturers_found:
            manufacturer_id = int(manufacturer['id_fabricante'])
            new_id = int(manufacturer['novo_id'])

            if current_id == manufacturer_id:
                return new_id
            else:
                continue

    def __update_manufacturers_id(self):

        for product in self.__selected_products:
            product['id_fabricante'] = int(self.__manufacturer_id)

    def __update_principles_description(self):

        for product in self.__selected_products:

            if product['id_principio_ativo'] is None:
                product['id_principio_ant'] = None
            else:
                current_id = int(product['id_principio_ativo'])
                new_id = self.__return_principle_new_id(current_id)

                if new_id:
                    product.update({'id_principio_ativo': new_id, 'id_principio_ant': None})
                else:
                    product.update({'id_principio_ant': current_id, 'id_principio_ativo': None})

    def __return_principle_new_id(self, current_id):

        for principle in self.__principles_found:
            principle_id = int(principle['id_principio_ativo'])

            if current_id == principle_id:
                return principle_id
            else:
                continue

    def __update_principles_id(self):

        for product in self.__selected_products:
            product['id_principio_ativo'] = int(self.__principle_id)

    def __product_treatment(self):

        for product in self.__selected_products:
            origin_product_bar = int(product['barras'])
            destiny_product_id = self.__comparison(origin_product_bar)

            if destiny_product_id is None:
                dates = {'inicio_promocao': product['inicio_promocao'],
                         'final_promocao': product['final_promocao'],
                         'data_cadastro': product['data_cadastro'],
                         'data_alteracao': product['data_alteracao']}

                treated_dates = self.__dates_treatment(dates)

                product.update({'inicio_promocao': treated_dates['inicio_promocao']})
                product.update({'final_promocao': treated_dates['final_promocao']})
                product.update({'data_cadastro': treated_dates['data_cadastro']})
                product.update({'data_alteracao': treated_dates['data_alteracao']})
                product.update({'novo_id': None})
                product.update({'comunicador': self.__communicator})
            else:
                product.update({'novo_id': destiny_product_id})

    def __comparison(self, origin_product_bar):

        for product in self.__products_comparison:
            destiny_product_bar = int(product['barras'])
            destiny_product_id = int(product['id_produto'])

            if origin_product_bar == destiny_product_bar:
                return destiny_product_id
            else:
                continue

    def __dates_treatment(self, dates):

        for key, date in dates.items():
            if date is None:
                pass
            else:
                if date == '0000-00-00':
                    new_date = datetime(1899, 12, 30)
                    formatted_date = new_date.strftime('%Y-%m-%d')
                    dates.update({key: formatted_date})
                else:
                    formatted_date = date.strftime('%Y-%m-%d')
                    dates.update({key: formatted_date})

        return dates

    def __data_selection(self):

        self.__selected_products_id = []
        self.__products_found = []

        for product in self.__selected_products:
            product_id = int(product['id_produto'])
            self.__selected_products_id.append(product_id)

            if product['novo_id'] is None:
                continue
            else:
                self.__products_found.append(product)

    def update_after_insert(self, products_after_insert, manufacturers_after_insert, principles_after_insert):

        manufacturer_data = []
        principle_data = []

        for product in self.__selected_products:
            product_id = int(product['id_produto'])
            new_product_id = self.__return_product_id(product_id, products_after_insert)

            if product['id_fabricante_ant'] is None:
                pass
            else:
                manufacturer_id = int(product['id_fabricante_ant'])
                new_manufacturer_id = self.__return_manufacturer_id(manufacturer_id, manufacturers_after_insert)
                manufacturer = {'campo': 'fabricante',
                                'valor': new_manufacturer_id,
                                'id_produto': new_product_id}
                manufacturer_data.append(manufacturer)

            if product['id_principio_ant'] is None:
                pass
            else:
                principio_id = int(product['id_principio_ant'])
                novo_principio_id = self.__return_principle_id(principio_id, principles_after_insert)
                principle = {'campo': 'principio_ativo',
                             'valor': novo_principio_id,
                             'id_produto': new_product_id}
                principle_data.append(principle)

        return {'manufacturer': manufacturer_data, 'principle': principle_data}

    def __return_product_id(self, product_id, products):

        for product in products:
            old_product_id = int(product['campo_auxiliar'])
            new_product_id = int(product['id_produto'])

            if product_id == old_product_id:
                return new_product_id
            else:
                continue

    def __return_manufacturer_id(self, manufacturer_id, manufacturers):

        for manufacturer in manufacturers:
            old_manufacturer_id = int(manufacturer['campo_auxiliar'])
            new_manufacturer_id = int(manufacturer['id_fabricante'])

            if manufacturer_id == old_manufacturer_id:
                return new_manufacturer_id
            else:
                continue

    def __return_principle_id(self, principio_id, principles):

        for principle in principles:
            old_principle_id = int(principle['campo_auxiliar'])
            new_principle_id = int(principle['id_principio_ativo'])

            if principio_id == old_principle_id:
                return new_principle_id
            else:
                continue

    def get_products(self):
        return self.__selected_products

    def get_products_id(self):
        return self.__selected_products_id

    def get_products_found(self):
        return self.__products_found
