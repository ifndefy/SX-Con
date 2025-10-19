import configparser as cparser
import pyodbc as odbc

class DatabaseConnection:
    def __init__(self):
        print("Initializing connectDB defaults...")

        #Create object to read from config file
        config = cparser.ConfigParser()

        config.read('config.ini')

        #fetch fields for connection string from config.ini
        self.odbc_driver = config.get('SQL Connection Parameters', 'odbc_driver')
        self.server_addr = config.get('SQL Connection Parameters', 'server_addr')
        self.server_port = config.get('SQL Connection Parameters', 'server_port')
        self.db_name_default = config.get('SQL Connection Parameters', 'db_name')
        self.db_user_default = config.get('SQL Connection Parameters', 'db_user')
        self.db_user_pass =  config.get('SQL Connection Parameters', 'db_user_pass')

    def establish_connection(self, 
                            driver = None, 
                            addr = None, 
                            port = None, 
                            db_name = None, 
                            db_user = None, 
                            user_pass = None):
        """
        Establishes a connection with the Azure SQL Database.

        [Args]: All arguments are optional, args not given will be fetched from default values in config.ini\n
            driver (string): Specifies the odbc driver to use for the connection, string in format \'{[driver name]}\'
            addr (string): Address of the server
            port (string): Server port being used
            db_name (string): Name of the specific database on the server
            db_user (string): The user connecting to the server, must exist as a valid user in the db
            user_pass (string): Password for db_user
        
        On success return 0, connection is established and stored in self.db_connection can be used to create cursors. Failures return -1 and no values are written to self.db_connection    
        """

        #if any specific values were not used, load from config instead 
        driver = driver or self.odbc_driver
        addr = addr or self.server_addr
        port = port or self.server_port
        db_name = db_name or self.db_name_default
        db_user = db_user or self.db_user_default
        ##todo: add popup to ask for password instead of hardcoding
        user_pass = user_pass or self.db_user_pass

        #Check if any connection string fields are null
        if not all([driver, addr, port, db_name, db_user, user_pass]):
            print("one or more required fields are null")
            return -1

        connection_string = f"Driver={driver};" \
                            f"Server={addr},{port};" \
                            f"Database={db_name};" \
                            f"Uid={db_user};" \
                            f"Pwd={user_pass};" \
                            f"Encrypt=yes;" \
                            f"TrustServerCertificate=no;" \
                            f"Connection Timeout=30;"
        
        self.db_connection = odbc.connect(connection_string)
        return 0
    
    def create_cursor(self):
        if self.db_connection is not None:
            return self.db_connection.cursor()
        else:
            print("Connection not established")

    def close_connection(self):
        if self.db_connection is not None:
            self.db_connection.close()
        else:
            print("Connection not found")
    
    def __del__(self):
        print("Cleaning up connectDB connection...")
        self.close_connection()
        

        

