from abc import ABC, abstractmethod
from typing import Type


class ConnectionInterface(ABC):

    @abstractmethod
    def connect_database(self, access_data: dict) -> dict:
        """Database Connection

        Returns:
            (In Success)
            Dict: {'return': 'Connected'} \n
            (In Fail)
            Dict: {'return': 'Exception', 'cod': some_error, 'description': some_description}
        """
        raise Exception('You cannot instance a Abstract Class')

    @abstractmethod
    def __return_error(self, error: Type[Exception]) -> dict:
        raise Exception('You cannot instance a Abstract Class')

    @abstractmethod
    def __return_success(self) -> dict:
        raise Exception('You cannot instance a Abstract Class')

    @abstractmethod
    def get_connection(self) -> Type[object]:
        """Get the connection

        Returns:
            Object: Pymysql object connection
        """
        raise Exception('You cannot instance a Abstract Class')
