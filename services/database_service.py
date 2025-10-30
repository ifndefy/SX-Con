from services import connectDB as db

class DatabaseService:
    def __init__(self):
        self.connection = None

    def connect(self):
        """
        :purpose: connect to the database
        :return: connection object
        :author(s): Maksym Komarov
        """
        self.connection = db.DatabaseConnection()
        self.connection.establish_connection()
        return self.connection

