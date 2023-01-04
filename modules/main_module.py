class MainModule():

    @staticmethod
    def _remove_erased(items):
        """Internal Function to remove erased data"""

        for item in items:
            if item['apagado'] == 'S':
                items.remove(item)
            else:
                continue
        return items

    @staticmethod
    def _communicator_treatment(communicator, items):
        """Internal Function to update communicator field"""

        for item in items:
            item.update({'comunicador': communicator})
        return items
