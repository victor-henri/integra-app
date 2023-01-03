class Partition:
    
    def __init__(self,
                 erased,
                 communicator,
                 products_id,
                 products_found,
                 products_after_insert,
                 origin_partition,
                 origin_branch_id,
                 destiny_branch_id):

        self.__erased = erased
        self.__communicator = communicator
        self.__products_id = products_id
        self.__products_found = products_found
        self.__products_after_insert = products_after_insert
        self.__origin_partition = origin_partition
        self.__origin_branch_id = origin_branch_id
        self.__destiny_branch_id = destiny_branch_id
        self.__selected_partitions = []

    def start_partition(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__extract_selected_data()
        self.__partition_treatment()

    def __remove_erased(self):

        for partition in self.__origin_partition:
            if partition['apagado'] == 'S':
                self.__origin_partition.remove(partition)
            else:
                continue

    def __extract_selected_data(self):

        for partition in self.__origin_partition:
            product_id = int(partition['id_produto'])
            partition_branch_id = int(partition['id_filial'])

            if product_id in self.__products_id and partition_branch_id == self.__origin_branch_id:
                self.__selected_partitions.append(partition)
            else:
                continue

    def __partition_treatment(self):

        for partition in self.__selected_partitions:
            old_id = int(partition['id_produto'])
            id_found = self.__return_new_id(old_id)

            if id_found is None:
                new_id = self.__return_id_after_insert(old_id)
                partition.update({'id_produto_ant': old_id})
                partition.update({'id_produto': new_id})
            else:
                partition.update({'id_produto_ant': partition['id_produto']})
                partition.update({'id_produto': id_found})

            datas = {'validade': partition['data_validade'], 
                     'fabricacao': partition['data_fabricacao']}

            treated_dates = self.__dates_treatment(datas)

            partition.update({'data_validade': treated_dates['validade']})
            partition.update({'data_fabricacao': treated_dates['fabricacao']})
            partition.update({'id_filial': self.__destiny_branch_id})
            partition.update({'comunicador': self.__communicator})

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

    def get_partition(self):
        return self.__selected_partitions
