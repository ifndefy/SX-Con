
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
        #print(connection)

        #redundant case, as if it fails at all, SPOT.OFFLINE is turned to True
        if connection is None:
            return -1

        elif SPOT.OFFLINE:
            return -1

        return 0

    except Exception as e:
        print(e)
        return -1

print(test_connect_database())