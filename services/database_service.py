import pyodbc
import struct
from azure.identity import DefaultAzureCredential

def get_conn():
        credential = DefaultAzureCredential(
            exclude_interactive_browser_credential=False
        )
        
        connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:sx-con-server-dev.database.windows.net,1433;"
            "Database=dev_db;Uid=SXCON_DEV;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        
        token = credential.get_token("https://database.windows.net/.default")
        token_bytes = token.token.encode("UTF-16-LE")
        token_struct = struct.pack(
            f'<I{len(token_bytes)}s', 
            len(token_bytes), 
            token_bytes
        )
        
        # This connection option is defined by microsoft in msodbcsql.h
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        
        conn = pyodbc.connect(
            connection_string, 
            attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct}
        )
        return conn

class DatabaseService:
    def __init__(self):
        print("Database init")