from .apputils import *


class PlaceholderApi:
    """Class for interacting with Jsonplaceholder"""
    
    def __init__(self) -> None:
        self.__base_url = "https://jsonplaceholder.typicode.com/"


    def todos(self, count: int = 1):
        """Max count: 200"""
        if count > 200:
            return "The number of data is less than 200"
        else:
            return get_todos(self.__base_url, count)

    def users(self, count: int = 1):
        """Max count: 10"""
        if count > 10:
            return "The number of data is less than 10"
        else:
            return get_users(self.__base_url, count)

    def posts(self, count: int = 1):
        """Max count: 100"""
        if count > 100:
            return "The number of data is less than 100"
        else:
            return get_posts(self.__base_url, count)

    def photos(self, count: int = 1):
        """Max count: 5000"""
        if count > 5000:
            return "The number of data is less than 5000"
        else:
            return get_photos(self.__base_url, count)

    def albums(self, count: int = 1):
        """Max count: 100"""
        if count > 100:
            return "The number of data is less than 100"
        else:
            return get_albums(self.__base_url, count)

    def comments(self, count: int = 1):
        """Max count: 500"""
        if count > 500:
            return "The number of data is less than 500"
        else:
            return get_comments(self.__base_url, count)