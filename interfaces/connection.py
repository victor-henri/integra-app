from abc import ABC, abstractmethod
from typing import TypedDict, Type


class AccessDatabase(TypedDict):
    host: str
    user: str
    password: str
    database: str
    port: int

class ConnectionInterface(ABC):

    @classmethod @abstractmethod
    def __connect_database(self):
        """_summary_

        Raises:
            Exception: _description_
        """
        raise Exception('You cannot instance a Abstract Class')

    @classmethod @abstractmethod
    def __return_error(self, error: Type[Exception]):
        """_summary_

        Args:
            error (Type[Exception]): _description_

        Raises:
            Exception: _description_
        """
        raise Exception('You cannot instance a Abstract Class')

    @classmethod @abstractmethod
    def __return_success(self):
        """_summary_

        Raises:
            Exception: _description_
        """
        raise Exception('You cannot instance a Abstract Class')

    @classmethod @abstractmethod
    def get_connection(self):
        """_summary_

        Raises:
            Exception: _description_
        """
        raise Exception('You cannot instance a Abstract Class')
