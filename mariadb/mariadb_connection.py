from typing import Type
import pymysql
from interfaces.connection import ConnectionInterface


class ConnectionMariaDb(ConnectionInterface):
    """Connection generator class - pymysql object"""

    def __init__(self):
        self.__connection = None


    def connect_database(self, access_data: dict) -> dict:
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
        """Get connection from pymysql object"""
        return self.__connection
