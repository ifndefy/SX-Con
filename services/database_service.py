from services import connect_database as db

class DatabaseService:
    def __init__(self):
        self.connection = None

    def connect(self, container_name: str):
        """
        :purpose: connect to a specific container in the database
        :param container_name: name of the container to connect to
        :return: connection object
        :author(s): Maksym Komarov
        """
        self.connection = db.DatabaseConnection()
        self.connection.establish_connection(container_name=container_name)
        return self.connection.container