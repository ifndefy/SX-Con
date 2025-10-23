from database_service import DatabaseService as Ds

def delete_record(table_name: str, key: str, unused: str) -> int :
    """"
    This function deletes a record from a table

    @param table_name: name of the table
    @param key: the location on the table
    @param unused: the unused value
    @return: 0 on success -1 on failure
    """
    try:
        print("deleting a record")
        conn = Ds.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM " + table_name + " WHERE " + key)

        conn.close()
    except Exception as e:
        return -1
    finally:
        return 0
