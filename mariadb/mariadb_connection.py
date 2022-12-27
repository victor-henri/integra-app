from typing import TypedDict, Type
from interfaces.connection import ConnectionInterface
import pymysql


class AccessDatabase(TypedDict):
    """Typing class
    """
    host: str
    user: str
    password: str
    database: str
    port: int


class ConnectionMariaDb(ConnectionInterface):
    """_summary_

    Args:
        ConnectionInterface (_type_): _description_
    """

    def __init__(self):
        self.__connection = None


    def connect_database(self, access_data: TypedDict[AccessDatabase]) -> dict:
        """Database Connection

        Returns:
            (In Success)
            Dict: {'return': 'Connected'} \n
            (In Fail)
            Dict: {'return': 'Exception', 'cod': some_error, 'description': some_description}
        """

        try:
            self.__connection = pymysql.connect(host=access_data['host'],
                                                user=access_data['user'],
                                                password=access_data['password'],
                                                database=access_data['database'],
                                                port=access_data['port'],
                                                charset='latin1',
                                                sql_mode="NO_ENGINE_SUBSTITUTION",
                                                cursorclass=pymysql.cursors.DictCursor)

            __log = self.__return_success
            return __log

        except Exception as error:
            __log = self.__return_error(error)
            return __log

    def __return_error(self, error: Type[Exception]) -> dict:
        return {'return': 'Exception', 'cod': error.args[0], 'description': error.args[1]}

    def __return_success(self) -> dict:
        return {'return': 'Connected'}

    def get_connection(self) -> Type[object]:
        """Get the connection

        Returns:
            Object: Pymysql object connection
        """
        return self.__connection
