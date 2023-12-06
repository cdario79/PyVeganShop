import os
import json


class _JsonDatabase:
    """
    This is a base class for manage JSON File like a database
    """

    _DATABASE_FOLDER = "database/"
    _DATABASE_PRODUCT_FILE = None
    _DATABASE_EMPTY_DATA = {"data": []}

    _is_same_instance = None

    def __new__(cls):
        """
        SINGLETON PATTERN
        check if class have an active instance
        if True return the active instance
        otherwise return new instance
        """

        if cls._is_same_instance is None:
            cls._is_same_instance = super().__new__(cls)

        return cls._is_same_instance

    def __init__(self):
        self._database_full_path = self._DATABASE_FOLDER + self._DATABASE_PRODUCT_FILE
        self._database_data = self._DATABASE_EMPTY_DATA

        self._create_database_folder()
        self._create_database_file()

        self._open()

    def _create_database_folder(self):
        """
        Create Database Folder if it does not exist
        """

        if not os.path.isdir(self._DATABASE_FOLDER):
            os.mkdir(self._DATABASE_FOLDER)

    def _create_database_file(self):
        """
        Create JSON File if it does not exist
        """

        if not os.path.isfile(self._database_full_path):
            self._save(self._DATABASE_EMPTY_DATA)

    def _save(self, data):
        """
        Save data to JSON File

        :param data: Dictionary
        """

        with open(self._database_full_path, "w", encoding='utf-8') as database_file:
            json.dump(data, database_file, indent=3)

    def _open(self):
        """
        Open JSON File and store it in a variable
        """

        with open(self._database_full_path, "r+", encoding='utf-8') as database_file:
            self._database_data = json.load(database_file)

    def load(self):
        """
        Read all content of database and return it

        :return: List of Dictionaries
        """

        return self._database_data["data"]

    def get_item_by_name(self, name):
        """
        Retrieve single item in database by his name

        :param name: string
        :return: Dictionary or Bool
        """

        for item in self._database_data["data"]:
            if item["name"].lower().strip() == name.lower().strip():
                return item
        return False

    def delete_by_name(self, name):
        """
        Delete single item in database by his name

        :param name: string
        """

        new_data = []

        for item in self._database_data["data"]:
            if item["name"].lower().strip() != name.lower().strip():
                new_data.append(item)

        self._database_data["data"] = new_data
        self._save(self._database_data)

    def insert(self, element):
        """
        Insert a new element in database

        :param element: Dictionary
        """

        saved_data = self._database_data["data"]
        saved_data.append(element)
        self._database_data["data"] = saved_data
        self._save(self._database_data)

    def update(self, element):
        """
        update an element in database

        :param element: Dictionary
        """

        new_data = []

        for item in self._database_data["data"]:
            if item["name"].lower().strip() == element["name"].lower().strip():
                new_data.append(element)
            else:
                new_data.append(item)

        self._database_data["data"] = new_data
        self._save(self._database_data)

    def upsert(self, element):
        """
        add if not exist or update if exist an element in database

        :param element: Dictionary
        """

        new_data = []
        product_exist = False

        for item in self._database_data["data"]:
            if item["name"].lower().strip() == element["name"].lower().strip():
                new_data.append(element)
                product_exist = True
            else:
                new_data.append(item)

        if not product_exist:
            new_data.append(element)

        self._database_data["data"] = new_data
        self._save(self._database_data)


class WarehouseDatabase(_JsonDatabase):
    """
    This class manage the database of warehouse data
    """

    _DATABASE_PRODUCT_FILE = "warehouse.json"


class SalesDatabase(_JsonDatabase):
    """
    This class manage the database of sales data
    """

    _DATABASE_PRODUCT_FILE = "sales.json"
