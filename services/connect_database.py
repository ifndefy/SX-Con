import configparser as cparser
import sys

from azure.cosmos import CosmosClient
from pathlib import Path
from src import SPOT
import utils.logger.logger as log
from utils.message_bus import status_bar_instance

class DatabaseConnection:
    _connections = {}

    def __init__(self):
        config = cparser.ConfigParser()
        current_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent
        config_path = current_dir / 'services' / 'config.ini'

        #Try to read the network config, on fail default to offline mode
        try:
            config.read(config_path)
            self.endpoint = config.get('Cosmos Connection Parameters', 'endpoint')
            self.database_name = config.get('Cosmos Connection Parameters', 'database_name')
            self.key = config.get('Cosmos Connection Parameters', 'key')
            self.client = CosmosClient(url=self.endpoint, credential=self.key)
            self.database = self.client.get_database_client(self.database_name)
            SPOT.OFFLINE = False
        except Exception as e:
            SPOT.OFFLINE = True
            self.client = None
            self.database = None
            status_bar_instance.send_message(f"Connection Error: Program starting in offline mode")

    def connect(self, container_name: str):
        if self.database is None:
            SPOT.OFFLINE = True
            return None

        try:
            if container_name not in self._connections:
                container = self.database.get_container_client(container_name)
                container.read()
                self._connections[container_name] = container
                log.debug(f"Connected to container: {container_name}")
            SPOT.OFFLINE = False  # reset on success
            return self._connections[container_name]
        except Exception as e:
            SPOT.OFFLINE = True
            log.debug(f"Could not connect to container: {container_name}")
            status_bar_instance.send_message(f"Connection Error: Could not connect to container: {container_name}")
            return None


# create a global instance
db_connection = DatabaseConnection()