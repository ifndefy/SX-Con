from services.connect_database import db_connection

class APIHandler:
    def __init__(self):
        self.db_connection = db_connection  # Add this line

    def process_action(self, action: str) -> str:
        return f"{action} executed."