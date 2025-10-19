import connectDB as db

class DatabaseService:
    def __init__(self):
        print("Database init")

    def connect(self):
        connection = db.DatabaseConnection()
        connection.establish_connection()
        return connection
