from services.database_service import DatabaseService

def get_max_value(table_name, column_name):
    """
    :purpose: returns the max value of a column in a table
    :return(s): the max value of a column in a table
    :author(s): Joe Lee
    """
    db_service = DatabaseService()
    db_service.connect()

    try:
        if db_service.connection is None:
            print("No connection established")
            return -1

        cursor = db_service.connection.create_cursor()
        query = f"SELECT MAX({column_name}) FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchone()

        if result[0] is not None:
            return result[0]
        else:
            return 0
    finally:
        if db_service.connection:
            db_service.connection.close_connection()