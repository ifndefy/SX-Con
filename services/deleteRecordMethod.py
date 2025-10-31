from database_service import DatabaseService


def delete_record(table_name: str, key: str, unused: str = '') -> int :
    """"
    This function deletes a record from a table

    @param table_name: name of the table
    @param key: the location on the table
    @param unused: the unused value, defaults to ''
    @return: 0 on success -1 on failure
    """
    try:
        print("deleting a record")
        Ds = DatabaseService()
        conn = Ds.connect()
        cursor = conn.create_cursor()
        cursor.execute(f"""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            where TABLE_NAME = '{table_name}'
            """)
        pk_result = cursor.fetchone()
        pk_column = pk_result[0]
        cursor.execute("DELETE FROM " + table_name + " WHERE " + pk_column + "=" + key)

        return 0
    except Exception as e:
        print("ERROR: failed to delete " + str(e))
        return -1
    finally:
        if conn:
            conn.close_connection()
