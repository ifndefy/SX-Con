import configparser as cparser

from azure.cosmos import CosmosClient
from pathlib import Path


class DatabaseConnection:
    def __init__(self):
        print("Initializing Cosmos DB connection...")
        self.client = None
        self.database = None
        self.container = None

        config = cparser.ConfigParser()
        current_dir = Path(__file__).parent
        config_path = current_dir / 'config.ini'

        try:
            config.read(config_path)
            self.endpoint = config.get('Cosmos Connection Parameters', 'endpoint')
            self.database_name = config.get('Cosmos Connection Parameters', 'database_name')
            self.container_name = config.get('Cosmos Connection Parameters', 'container_name')
            self.key = config.get('Cosmos Connection Parameters', 'key')
        except Exception as e:
            print(f"Error fetching from config.ini: {e}")

    def establish_connection(self, endpoint=None, database_name=None, container_name=None, key=None):
        """
        :purpose: Connect the object to the database to enable communications between the program and the database
        :author(s): Maksym Komarov, Joe Lee
        """
        endpoint = endpoint or self.endpoint
        database_name = database_name or self.database_name
        container_name = container_name or self.container_name
        key = key or self.key

        if not all([endpoint, database_name, container_name, key]):
            print("One or more required fields are null")
            return -1

        try:
            self.client = CosmosClient(url=endpoint, credential=key)
            self.database = self.client.get_database_client(database_name)
            self.container = self.database.get_container_client(container_name)
            print("Cosmos DB connection established")
            return 0
        except Exception as e:
            print(f"Failed to establish Cosmos DB connection: {e}")
            return -1