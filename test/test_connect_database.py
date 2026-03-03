
from services.connect_database import db_connection
from src import SPOT

def test_connect_database():
    """
    purpose: test the success of the database connection
    return: 0 on success, else -1
    author: Tyler Slagboom
    """
    try:
        connection_target = "test"
        connection = db_connection.connect(connection_target)

        if connection is None:
            return -1

        elif SPOT.OFFLINE:
            return -1

        connection_target = ""
        connection = db_connection.connect(connection_target)

        if connection is None:
            return -1

        elif SPOT.OFFLINE:
            return -1

        connection_target = "123abc098zyx"
        connection = db_connection.connect(connection_target)

        if connection is None:
            return -1

        elif SPOT.OFFLINE:
            return -1

        connection_target = "Entities"
        connection = db_connection.connect(connection_target)

        if connection is None:
            return -1

        elif SPOT.OFFLINE:
            return -1

        return 0

    except Exception as e:
        print(e)
        return -1