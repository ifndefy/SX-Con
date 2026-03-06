
from services.connect_database import db_connection
from src import SPOT

def test_connect_database():
    """
    purpose: test the success of the database connection
    return: 0 on success, else -1
    author: Tyler Slagboom
    """
    connection_target = "test"
    connection = db_connection.connect(connection_target)

    if connection is not None:
        assert False, f"Expected failure to connect to false database container {connection_target}"

    elif not SPOT.OFFLINE:
        assert False, "Expected SPOT.OFFLINE to be set to True"

    connection_target = ""
    connection = db_connection.connect(connection_target)

    if connection is not None:
        assert False, f"Expected failure to connect to false database container {connection_target}"

    elif not SPOT.OFFLINE:
        assert False, "Could not connect to database"


    connection_target = "123abc098zyx"
    connection = db_connection.connect(connection_target)

    if connection is not None:
        assert False, f"Expected failure to connect to false database container {connection_target}"

    elif not SPOT.OFFLINE:
        assert False, "Expected SPOT.OFFLINE to be set to True"

    connection_target = "Entities"
    connection = db_connection.connect(connection_target)

    if connection is None:
        assert False, f"Expected to be able to connect to {connection_target}"

    elif SPOT.OFFLINE:
        assert False, f"Expected to be able to connect to {connection_target}"