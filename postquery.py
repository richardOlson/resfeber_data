# This is the file that is used to query the database
import psycopg2
from settings import password, username, database

# building a class that can query the database
class QueryPostgres:

    
    # This function will contain the info that is needed to communicate with the server
    def __init__(self, password=None , user = None, host="127.0.0.1", port="5432", database=None):
        self.password=password
        self.user=user
        self.host=host
        self.port=port
        self.database=database
        self.conn=None
        self.cursor=None
        self.connectionsDict = {"password": self.password, "user":self.user, 
                                "host":self.host, "port":self.port, 
                                "database":self.database, "conn":self.conn, "cursor":self.cursor}
        # this is to just check what the password is
        print(f"this is from self.password {self.password}")


    def fill_connect_vals(self, **kwargs):
        """
        This is a function that can be used to fill
        in any of the connection arguments that may have not already been filled.
        This function will able the user to input the "password", "user", "host", "port",  "database", 
        "cursor", and "conn" (theConnection object)
        """
        for keyWord, val in kwargs.items():
            # checking to which of the self values it matches the connection dictionary
            if keyWord in self.connectionsDict:
                self.connectionsDict[keyWord] = val 
            

    def return_connection_vals(self)-> str:
        """
        Will return the values that are stored in the form of a dictionary
        """
        theString = ""
        for key, val in self.connectionsDict.items():
            if key not in ["conn", 'cursor']:
                if key == "database":
                    key = "dbname" # used to change the name to dbname for the connection
                theString + key + "=" + str(val) + " "
        theString = theString.strip()
        return theString


    def get_connection(self):
        """
        Returns the connection object that is held by the class
        """
        return self.conn

    
    def get_cursor(self):
        """
        Returns the cursor object that is held by the class
        """
        return self.cursor


    def createConnection(self):
        """
        This function will create the connection and will also create the cursor
        """
        try:
            connection = psycopg2.connect(self.return_connection_vals())
      
        except (Exception, psycopg2.Error) as error :
            #closing database connection.
            if(connection):
                connection.close()
                print("PostgreSQL connection is closed")

            print ("Error while connecting to PostgreSQL", error)
        
        cursor = connection.cursor()
        self.cursor = cursor
        self.conn = connection

    
        
        
if __name__ == "__main__":

    print(username)
    print(password)
    print(type(password))
    d = QueryPostgres(password=password, user=username, database="airbnb")      
    #d.createConnection()