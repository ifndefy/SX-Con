from services.database_service import DatabaseService


def insert_record(table_name: str, attribute_pairs: dict, unused: str = ""):
    """
    :purpose: inserts any record into the database
    :param: table_name: name of the table
    :param: attribute_pairs: dictionary of attribute names and values
    :param: unused: optional unused value
    :author(s): Joe Lee
    """

    try:
        db_service = DatabaseService()
        conn = db_service.connect()
        cursor = conn.create_cursor()

        columns = ", ".join(attribute_pairs.keys())
        num_vals = ", ".join(['?'] * len(attribute_pairs))

        # converts to string then creates a tuple with them
        values = tuple(str(v) for v in attribute_pairs.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({num_vals})"

        cursor.execute(query, values)
        cursor.commit()

    except Exception as e:
        print(f"Error in insert_record: {e}")
        return "-1"
    finally:
        if conn:
            conn.close_connection()