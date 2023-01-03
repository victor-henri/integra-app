class Customer:

    def __init__(self, erased, communicator, origin_customers):

        self.__erased = erased
        self.__communicator = communicator
        self.__origin_customers = origin_customers
        self.__selected_customers_id = ()

    def start_customer(self):

        if self.__erased is True:
            self.__remove_erased()

        self.__customer_treatment()
        self.__extract_customers_id()

    def __remove_erased(self):

        for customer in self.__origin_customers:
            if customer['apagado'] == 'S':
                self.__origin_customers.remove(customer)
            else:
                continue

    def __customer_treatment(self):

        for customer in self.__origin_customers:
            dates = {'data_nascimento': customer['data_nascimento'],
                     'data_cadastro': customer['data_cadastro'],
                     'data_alteracao': customer['data_alteracao']}

            other_fields = {'nome': customer['nome'],
                            'endereco': customer['endereco']}

            treated_dates = self.__dates_treatment(dates)
            treated_fields = self.__fields_treatment(other_fields)

            customer.update({'data_nascimento': treated_dates['data_nascimento']})
            customer.update({'data_cadastro': treated_dates['data_cadastro']})
            customer.update({'data_alteracao': treated_dates['data_alteracao']})
            customer.update({'nome': treated_fields['nome']})
            customer.update({'endereco': treated_fields['endereco']})
            customer.update({'comunicador': self.__communicator})

    def __dates_treatment(self, dates):

        for key, date in dates.items():
            if date is None:
                pass
            else:
                formatted_date = date.strftime('%Y-%m-%d')
                dates.update({key: formatted_date})

        return dates

    def __fields_treatment(self, other_fields):

        characters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                      'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                      'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ')

        for key, field in other_fields.items():

            if field is None:
                pass
            else:
                values = []

                for caracter in field:
                    if caracter in characters:
                        values.append(caracter)

                formatted_field = ''.join(values)
                other_fields.update({key: formatted_field})

        return other_fields

    def __extract_customers_id(self):

        temporary_customers = []

        for customer in self.__origin_customers:
            temporary_customers.append(customer['id_cliente'])

        self.__selected_customers_id = tuple(temporary_customers)

    def get_customers(self):
        return self.__origin_customers

    def get_customers_id(self):
        return self.__selected_customers_id
