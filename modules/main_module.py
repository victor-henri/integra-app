class MainModule():

    @staticmethod
    def _remove_erased(registers):
        """Internal Function to remove erased data"""

        for register in registers:
            if register['apagado'] == 'S':
                registers.remove(register)
            else:
                continue

        return registers

    @staticmethod
    def _communic_treatment(communicator, registers):
        """Internal Function to update communicator field"""

        for register in registers:
            register.update({'comunicador': communicator})

        return registers

    @staticmethod
    def _extract_data(registers, products_id, origin_branch_id=None):

        extract_data = []

        if origin_branch_id is not None:

            for register in registers:
                product_id = int(register['id_produto'])
                branch_id = int(register['id_filial'])

                if product_id in products_id and branch_id == origin_branch_id:
                    extract_data.append(register)
                else:
                    continue
        else:
            for register in registers:
                product_id = int(register['id_produto'])

                if product_id in products_id:
                    extract_data.append(register)
                else:
                    continue

        return extract_data
