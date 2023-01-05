from .main_module import MainModule


class Principle(MainModule):

    def __init__(self, erased, communicator, origin_principles, destiny_principles):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_principles = origin_principles
        self.__destiny_principles = destiny_principles
        self.__principles_found = []
        self.__principles_not_found = []

    def start_principle(self):

        if self.__erased is True:
            self.__origin_principles = self._remove_erased(self.__origin_principles)

        self.__search_principles()
        self.__principles_not_found = self._communic_treatment(self.__communicator,
                                                               self.__principles_not_found)

    def __search_principles(self):

        for principle in self.__origin_principles:
            new_id = self.__return_principle(principle['descricao'])

            if new_id:
                principle.update({'novo_id': new_id})
                self.__principles_found.append(principle)
            else:
                principle.update({'novo_id': None})
                self.__principles_not_found.append(principle)

    def __return_principle(self, origin_description):

        for principle in self.__destiny_principles:
            destiny_description = principle['descricao']
            principle_id = int(principle['id_principio_ativo'])

            if origin_description == destiny_description:
                return principle_id
            else:
                continue

    def get_principles_found(self):
        return self.__principles_found

    def get_principles_not_found(self):
        return self.__principles_not_found
