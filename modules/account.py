class Account:

    def __init__(self,
                 erased,
                 communicator,
                 origin_branch_id,
                 destiny_branch_id,
                 origin_accounts):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_branch_id = origin_branch_id
        self.__destiny_branch_id = destiny_branch_id
        self.__origin_accounts = origin_accounts

    def start_account(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__acount_treatment()

    def __remove_erased(self):

        for account in self.__origin_accounts:
            if account['apagado'] == 'S':
                self.__origin_accounts.remove(account)
            else:
                continue

    def __acount_treatment(self):

        for account in self.__origin_accounts[:]:
            branch_id = int(account['id_filial'])

            if branch_id != self.__origin_branch_id:
                self.__origin_accounts.remove(account)
            else:
                dates = {'data_venda': account['data_venda'],
                         'vencimento': account['vencimento'],
                         'data_baixa': account['data_baixa'],
                         'data_cadastro': account['data_cadastro'],
                         'data_alteracao': account['data_alteracao']}

                treated_dates = self.__dates_treatment(dates)

                account.update({'data_venda': treated_dates['data_venda']})
                account.update({'vencimento': treated_dates['vencimento']})
                account.update({'data_baixa': treated_dates['data_baixa']})
                account.update({'data_cadastro': treated_dates['data_cadastro']})
                account.update({'data_alteracao': treated_dates['data_alteracao']})
                account.update({'id_filial': self.__destiny_branch_id})
                account.update({'comunicador': self.__communicator})

    def __dates_treatment(self, dates):

        for key, date in dates.items():
            if date is None:
                pass
            else:
                formatted_date = date.strftime('%Y-%m-%d')
                dates.update({key: formatted_date})

        return dates

    def get_accounts(self):
        return self.__origin_accounts
