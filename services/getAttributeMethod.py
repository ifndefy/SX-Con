from dotenv import load_dotenv
from database_service import DatabaseService

load_dotenv()


def get_attribute_value(table_name: str, attribute: str, pk: str) -> str:
    """
    Takes 3 string inputs (20 CHAR each)

    table_name to represent the table to select from
    attribute to represent the value to select
    pk to represent the primary key to filter by
    """
    conn = None
    try:
        db = DatabaseService()
        conn = db.connect()
        cursor = conn.create_cursor()

        # Find the pk column in {table_name}
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = '{table_name}' 
        """)
        pk_result = cursor.fetchone()
        pk_column = pk_result[0]

        # Set the query filtering by pk
        query = f"SELECT {attribute} FROM {table_name} WHERE {pk_column} = {pk}"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return str(result[0])
        return "-1"

    except Exception as e:
        print(f"Error in get_attribute_value: {e}")
        return "-1"
    finally:
        if conn:
            conn.close_connection()