import os
import pyodbc
from typing import Union
from dotenv import load_dotenv
from database_service import get_conn


load_dotenv()


def get_record(table_name: str, primary_key: str, unused: str) -> Union[dict, str]:
    """
    Takes 3 string inputs (20 CHAR each)

    one to represent the table to select from

    one to represent the primary key or unique key

    unused/for future use

    Errors returns “-1”
    """

    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Query the database for all columns
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        cursor.execute(query, (primary_key,))
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
            conn.close()