import configparser as cparser
import pyodbc as odbc
import struct
from azure.identity import DefaultAzureCredential
from pathlib import Path


class DatabaseConnection:
    def __init__(self):
        print("Initializing connectDB defaults...")

        self.db_connection = None

        config = cparser.ConfigParser()

        current_dir = Path(__file__).parent
        config_path = current_dir / 'config.ini'

        try:
            config.read(config_path)

            self.odbc_driver = config.get('SQL Connection Parameters', 'odbc_driver')
            self.server_addr = config.get('SQL Connection Parameters', 'server_addr')
            self.server_port = config.get('SQL Connection Parameters', 'server_port')
            self.db_name_default = config.get('SQL Connection Parameters', 'db_name')
            self.sql_access_token = config.getint('SQL Connection Parameters','sql_access_token')
        except Exception as e:
            print(f"Error fetching from config.ini: {e}")

    def establish_connection(self, 
                            driver = None, 
                            addr = None, 
                            port = None, 
                            db_name = None, 
                            access_mode = None):
        """
        Establishes a connection with the Azure SQL Database.

        [Args]: All arguments are optional, args not given will be fetched from default values in config.ini\n
            driver (string): Specifies the odbc driver to use for the connection, string in format \'{[driver name]}\'
            addr (string): Address of the server
            port (string): Server port being used
            db_name (string): Name of the specific database on the server
            db_user (string): The user connecting to the server, must exist as a valid user in the db
            access_mode (int): used to identify what form of authentication is being used, almost no reason to ever change  
        
        On success return 0, connection is established and stored in self.db_connection can be used to create cursors. Failures return -1 and no values are written to self.db_connection    
        """

        #if any specific values were not used, load from config instead 
        driver = driver or self.odbc_driver
        addr = addr or self.server_addr
        port = port or self.server_port
        db_name = db_name or self.db_name_default
        access_mode = access_mode or self.sql_access_token

        #Check if any connection string fields are null
        if not all([driver, addr, port, db_name, access_mode]):
            print("one or more required fields are null")
            return -1
        credential = DefaultAzureCredential(
            exclude_interactive_browser_credential=True
        )
        connection_string = f"Driver={driver};" \
                            f"Server={addr},{port};" \
                            f"Database={db_name};" \
                            "Encrypt=yes;" \
                            "TrustServerCertificate=no;" \
                            "Connection Timeout=30"

        token = credential.get_token("https://database.windows.net/.default")
        token_bytes = token.token.encode("UTF-16-LE")

        token_struct = struct.pack(f'<I{len(token_bytes)}s', 
                                   len(token_bytes), 
                                   token_bytes)

        try:
            self.db_connection = odbc.connect(connection_string, attrs_before={access_mode: token_struct})
        except:
            print("Failed to establish connection")
            return -1
        
        return 0

    def create_cursor(self):
        if self.db_connection is not None:
            return self.db_connection.cursor()
        else:
            print("Connection not established")

    def close_connection(self):
        if self.db_connection is not None:
            print("Closing connection")
            self.db_connection.close()
        else:
            print("Connection not found")
