from typing import Union
from dotenv import load_dotenv
from services.database_service import DatabaseService

load_dotenv()


def get_record(table_name: str, primary_key: str, unused: str = "") -> Union[dict, str]:
    """
    Takes 3 string inputs (20 CHAR each)
    one to represent the table to select from
    one to represent the primary key or unique key
    unused/for future use
    Errors returns “-1”
    """
    try:
        db_service = DatabaseService()
        conn = db_service.connect()
        cursor = conn.create_cursor()

        # Find the pk column in {table_name}
        cursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = '{table_name}' 
        """)
        pk_result = cursor.fetchone()
        pk_column = pk_result[0]

        # Query the database for all columns
        query = f"SELECT * FROM {table_name} WHERE {pk_column} = {primary_key}"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # Get column names from cursor description
            columns = [column[0] for column in cursor.description]
            # Convert row to dictionary
            record = dict(zip(columns, result))
            return record
        return "-1"
        
    except Exception as e:
        print(f"Error in get_record: {e}")
        return "-1"
    finally:
        if conn:
            conn.close_connection()