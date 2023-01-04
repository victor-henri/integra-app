from .main_module import MainModule


class Bill(MainModule):

    def __init__(self,
                 erased,
                 communicator,
                 origin_bills,
                 origin_branch_id,
                 destiny_branch_id,
                 suppliers_found,
                 suppliers_after_insert):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_bills = origin_bills
        self.__origin_branch_id = origin_branch_id
        self.__destiny_branch_id = destiny_branch_id
        self.__suppliers_found = suppliers_found
        self.__suppliers_after_insert = suppliers_after_insert

    def start_bill(self):

        if self.__erased is True:
            self.__origin_bills = self._remove_erased(self.__origin_bills)

        self.__bills_treatment()
        self.__update_suppliers_id()

    def __bills_treatment(self):

        for bill in self.__origin_bills[:]:
            branch_id = int(bill['id_filial'])

            if branch_id != self.__origin_branch_id:
                self.__origin_bills.remove(bill)
            else:
                dates = {'data_emissao': bill['data_emissao'],
                         'data_vencimento': bill['data_vencimento'],
                         'data_pagamento': bill['data_pagamento']}

                treated_dates = self.__dates_treatment(dates)

                bill.update({'data_emissao': treated_dates['data_emissao']})
                bill.update({'data_vencimento': treated_dates['data_vencimento']})
                bill.update({'data_pagamento': treated_dates['data_pagamento']})
                bill.update({'id_filial': self.__destiny_branch_id})
                bill.update({'comunicador': self.__communicator})

    def __dates_treatment(self, dates):

        for key, date in dates.items():
            if date is None:
                pass
            elif date == '0000-00-00':
                pass
            else:
                formatted_date = date.strftime('%Y-%m-%d')
                dates.update({key: formatted_date})

        return dates

    def __update_suppliers_id(self):

        for bill in self.__origin_bills:
            current_id = int(bill['id_fornecedor'])
            new_id = self.__return_supplier_new_id(current_id)

            if new_id:
                bill.update({'id_fornecedor': new_id})
            else:
                id_after_insert = self.__return_id_after_insert(current_id)
                bill.update({'id_fornecedor': id_after_insert})

    def __return_supplier_new_id(self, current_id):

        for supplier in self.__suppliers_found:
            supplier_id = int(supplier['id_fornecedor'])
            new_id = int(supplier['novo_id'])

            if current_id == supplier_id:
                return new_id
            else:
                continue

    def __return_id_after_insert(self, current_id):

        for supplier in self.__suppliers_after_insert:
            supplier_id = int(supplier['id_fornecedor'])
            old_id = int(supplier['campo_auxiliar'])

            if current_id == old_id:
                return supplier_id
            else:
                continue

    def get_bills(self):
        return self.__origin_bills
