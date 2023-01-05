from .main_module import MainModule


class Company(MainModule):

    def __init__(self, erased, communicator, origin_companies):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_companies = origin_companies

    def start_company(self):

        if self.__erased is True:
            self.__origin_companies = self._remove_erased(self.__origin_companies)

        self.__origin_companies = self._communic_treatment(communicator=self.__communicator,
                                                           registers=self.__origin_companies)

    def get_companies(self):
        return self.__origin_companies
