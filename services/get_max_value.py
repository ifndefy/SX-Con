from services.database_service import DatabaseService

def get_max_value(table_name, column_name):
    """
    :purpose: returns the max value of a column in a table
    :return(s): the max value of a column in a table
    :author(s): Joe Lee
    """
    try:
        db_service = DatabaseService()
        db_service.connect()
    except Exception as e:
        print(e)
        return -1

    try:
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