import configparser as cparser

from azure.cosmos import CosmosClient
from pathlib import Path
import utils.logger as log


class DatabaseConnection:
    _connections = {}

    def __init__(self):
        config = cparser.ConfigParser()
        current_dir = Path(__file__).parent
        config_path = current_dir / 'config.ini'
        config.read(config_path)
        self.endpoint = config.get('Cosmos Connection Parameters', 'endpoint')
        self.database_name = config.get('Cosmos Connection Parameters', 'database_name')
        self.key = config.get('Cosmos Connection Parameters', 'key')
        self.client = CosmosClient(url=self.endpoint, credential=self.key)
        self.database = self.client.get_database_client(self.database_name)

    def connect(self, container_name: str):
        if container_name not in self._connections:
            self._connections[container_name] = self.database.get_container_client(container_name)
            log.debug(f"Connected to container: {container_name}")
        return self._connections[container_name]


# create a global instance
db_connection = DatabaseConnection()