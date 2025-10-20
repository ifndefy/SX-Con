import os
import pyodbc
from dotenv import load_dotenv
from database_service import get_conn

load_dotenv()


def get_attribute_value(table_name: str, key: str, unused: str) -> str:
    """
    Takes 3 string inputs (20 CHAR each)

    one to represent the table to select from
    one to represent the key
    unused/for future use
    """
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Query the database
        query = f"SELECT value FROM {table_name} WHERE id = ?"
        cursor.execute(query, (key,))
        result = cursor.fetchone()

        if result:
            return str(result[0])
        return "-1"
        
    except Exception as e:  # Fixed: capture exception as 'e'
        print(f"Error in get_attribute_value: {e}")
        return "-1"
    finally:
        if conn:
            conn.close()  # Connection close
    
    