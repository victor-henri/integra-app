class Company:

    def __init__(self, erased, communicator, origin_companies):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_companies = origin_companies

    def start_company(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__company_treatment()

    def __remove_erased(self):

        for company in self.__origin_companies:
            if company['apagado'] == 'S':
                self.__origin_companies.remove(company)
            else:
                continue

    def __company_treatment(self):

        for company in self.__origin_companies:
            company.update({'comunicador': self.__communicator})

    def get_companies(self):
        return self.__origin_companies
