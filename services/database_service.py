from services import connectDB as db

class DatabaseService:
    def __init__(self):
        self.connection = None
        print("Database init")

    def connect(self):
        self.connection = db.DatabaseConnection()
        self.connection.establish_connection()
        return self.connection

