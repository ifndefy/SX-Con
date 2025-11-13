from database_service import DatabaseService

def delete_attribute(table_name: str, attr: str, key: str ) -> int:
    """"
    This function deletes a attribute from a record from the database.

    #param table_name: the name of the table
    #param attr: the name of the attribute
    #param key: the location of the record
    #return: -1 on failure
    """

    try:
        print("deleting an attribute")
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
        cursor.execute("UPDATE " + table_name + " SET " + attr + " = NULL WHERE " + pk_column + " = " + key)
        cursor.connection.commit()
    except Exception as e:
        print("Error: failed to delete an attribute " + str(e))
        return -1
    finally:
        if conn:
            conn.close_connection()
