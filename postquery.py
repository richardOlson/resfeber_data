# This is the file that is used to query the database
import psycopg2
from psycopg2 import sql
from settings import password, username, database


# This class will help with the building and adding of rows to the table
# It does this by adding constructing the string the will be used in the sql 
# query
class QueryStrings:
    def __init__(self, tableName=None, colNames=None):
        self.tableName = tableName
        self.colNames = colNames
        self.prinmary_key = None



    def put_colNames_tableName_primary_key(self, colNames, tableName, prinmary_key=None):
        """
        This function is used to put in the column and the table names so that 
        the other functions can be used
        """
        self.tableName= tableName
        self.colNames = colNames
        

    def create_table(self, tableName, primaryKey=None, Nullable=[], colNames=None, ):
        """
        This is the method that will be used to create a table.
        tableName:  This is a string of the table that you want to create
        primaryKey:  enter wich of the column names you would like to be a primary key if any.
        Nullable:   This expects a list of those colNames that can be Nullable, if empty all cols will be non_nullable.
        colNames:   This expects a list of lists, with value 0 being the column name and the values after that being data type in 
        element 1 and then other column constraints after that or Unique 1 being the data type.

        Returns:    Will return the string used in the exucute function to make a table with the columns that you want

        """
        self.colNames = colNames
        self.tableName = tableName
        self.prinmary_key = primaryKey # setting the attribute primary key
        # using the sql version of the formated string to do this
        # queryString = sql.SQL("INSERT INTO {tableName} ({cols}) VALUES ({col_vals})").format(
        #                     tableName=  sql.Identifier(self.tableName),
        #                     cols = sql.SQL(",").join(map(sql.Identifier, columnsString)),
        #                     col_vals = sql.SQL(",").join(map(sql.Identifier, dataRow))
        #                     )
        
        if colNames == None:
            raise Exception("There are no colums secified for the table")
        # Will loop through  and build the colums and the types
        # if colNames:
        #     for i in range(len(colNames)):
        #         queryString = queryString +  colNames[i][0] + " " + colNames[i][1]
        #         if primaryKey == colNames[i][0]:
        #             queryString = queryString + " " + "PRIMARY KEY"
        #         if colNames[i][0] not in Nullable:
        #             queryString = queryString + " NOT NULL"
        #         if i < len(colNames)-1:
        #             queryString =  queryString + ", "
        # queryString = queryString + ")"
        # Will make a list that has the element of each colum
        colList = []
        for i in range(len(colNames)):
            theString = ""
            theString += colNames[i][0] + " " + colNames[i][1]
            if colNames[i][0] == primaryKey:
                # building the column that is the primary key
                theString += " PRIMARY KEY"
            if colNames[i][0] not in Nullable: # default is a empty list
                theString += " NOT NULL"
            colList.append(theString)


        queryString = sql.SQL(
                                "CREATE TABLE IF NOT EXISTS {} ({cols})".format(sql.Literal(self.tableName),
                                cols = sql.SQL(", ").join(map(sql.Identifier, colList))
                                )
        )
        # queryString = f"CREATE TABLE [IF NOT EXISTS] {tableName} ("
        # # will now loop throught colNames and will add them to the query string
        
        return queryString


    # def __col_names_in_paren_string(self, drop_primary_key=True):
        # """
        # This function will make the column names in a parenthesis enclosed list to be
        # used for making the insert statement
        # to inert into a table
        # Will return None if there are no colnames of the tablename
        # Will also return None if there are not a tablename specified
        # """
        # if self.colNames == None or self.tableName == None:
            # return None
        # theString = "("
        #looping through and creating the paren list of the column names
        # for i, name in enumerate(self.colNames):
            # theString +=  name 
            # if i < len(self.colNames)-1:
                # theString += ", "
        # theString += ")"
        # return theString


    def get_col_names(self, drop_primary_key=True):
        """
        This function will return the column names in a list format of the table 
        the instance of the class is associated with.
        This function will not make a query to the sql.
        This function has the ability of removing the primary key from the list of the 
        columns if needed.

        Returns:    Will return a list of the colum names, Will return an empty list if there
        are no table associated with this instance.
        """
        if self.tableName == None or self.colNames == None:
            return []
        newList = []
        for colname in self.colNames:
            if colname != self.prinmary_key:
                newList.append(colname)
        return newList


    def insert_to_table(self, dataRow, val_not_in_primary_key=True):
        """
        This function will make the string which then can be used to isnert a data into 
        a postgresql database

        dataRow will be a list or lists or tuples.  The inner list will represent a row.
            
        colNames will be a list of the columnNames
        """
        # checking to make sure there is a tableName and the column names to use in the string
        if self.colNames == None:
            raise Exception("No column names are supplied.")
        if self.tableName == None:
            raise Exception("No tableName has been supplied.")
        
        columnsString = self.get_col_names() # can drop the col
                                               # if is aoutincremented in 
                                               # the database
        # creating the sql for the values being put in the col_vals
        theData = [] # this is used to pass in the data to the query string below
        for row in dataRow:
            theData.append(sql.SQL("({the_val})".format(the_val = sql.SQL(",").join(map(sql.Identifier, row)))))

        #To see the string version of this will need to do the queryString.as_string("putConnection_here")
        queryString = sql.SQL("INSERT INTO {tableName} ({cols}) VALUES {col_vals}").format(
                            tableName=  sql.Identifier(self.tableName),
                            cols = sql.SQL(",").join(map(sql.Identifier, columnsString)),
                            col_vals = sql.SQL(",").join(map(sql.Identifier, theData))
                            )
        # queryString = "INSERT INTO {self.tableName} {columnsString} VALUES "
        # # building the Values list
        # valueString = "("
        # # looping 
        # for i, value in enumerate(dataRow):
        #     if val_not_in_primary_key and value == self.prinmary_key:
        #         continue
        #     quote = ""
        #     if isinstance(value, str):
        #         quote = "\""
        #     valueString +=  f"{quote}{value}{quote}"
        #     if i < len(dataRow)-1:
        #         valueString += ", "
        # valueString += ")"
        # queryString += valueString
        return queryString



    def colNames_string_query(self, tableName):
        # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'some_table';
        """
        This function will return sql.SQL object to make a column name query.
        
        Will return "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "
        """
        theString = sql.SQL("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = {table_Name}").format(
            table_Name = sql.Identifier(tableName)
        )
        # This is returning a sql SQL object -- to see the string need to do
        # SQL_object.as_string(the_connection_passed_in_here)
        return theString




    

    
    


# building a class that can query the database
class QueryPostgres:

    
    # This function will contain the info that is needed to communicate with the server
    def __init__(self, password=None , user = None, host="127.0.0.1", port="5432", database=None, table_name=None):
        self.password=password
        self.user=user
        self.host=host
        self.port=port
        self.database=database
        self.conn=None
        self.cursor=None
        self.tableName = table_name
        self.connectionsDict = {"password": self.password, "user":self.user, 
                                "host":self.host, "port":self.port, 
                                "database":self.database, "conn":self.conn, "cursor":self.cursor}
        self.prinmary_key = None
        self.query_builder = QueryStrings() # building the query builder in the class to user to make the strings
        


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
                theString = theString + key + "=" + str(val) + " "
               # breakpoint()
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

    def get_col_names(self, query_first=False, table_Name=None):
        """
        This function will return the column names in a list.
        If the query builder class has a list of column names associated with it, 
        it will use that list. If there are no tables associated with the query builder class,
        then it will make a query to the table.  
        If no table_name is passed in, it will use the table name associated with the query builder class.
        This function can be set to skip using the col_names in the query_builder class and go 
        directly to querying the table first with having query_first == True.
        
        Returns empty list if no columns or will return the columns in a list format
        """
        theReturnList = []
        # getting the tablename
        if table_Name == None:
            table_Name = self.query_builder.tableName
        # getting the columns from the query builder class
        if query_first == False:
            theList = self.query_builder.get_col_names(drop_primary_key=False)
            if theList: # if the list is not empty then it will return the list here
                return theList
        # if here will make the request to postgres database and get the column names from there
        sql_object = self.query_builder.colNames_string_query(table_Name)
        # making the call to the database
        self.cursor.execute(sql_object)
        # getting the list of tuples
        col_list = self.cursor.fetchall()
        # making the list
        for theTup in col_list:
            theReturnList.append(theTup[0])
        
        return theReturnList



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


    
    def close(self):
        """
        This function will close the cursor and the connection object
        """
        self.cursor.close()
        self.conn.close()  


    def work_with_table(self, tableName):
        """
        This function will cause the querybuilder to contain the table name
        supplied.
        """ 
        # seeting the query builder that is associated with the QueryPostgres
        # to be set
        self.query_builder.tableName = tableName


if __name__ == "__main__":


    
    d = QueryPostgres(password=password, user=username, database="airbnb_data") 
    print(d.return_connection_vals())     
    d.createConnection()
    c = d.get_cursor()
    #c.execute('SELECT version()')
    #print(c.fetchall()) # showing the version of the database
    
    
    
    s = QueryStrings(tableName='airbnb')
    # creating the table
    sql_object = s.create_table(tableName="airbnb", primaryKey="Id", colNames=[["Id", "serial" ],["lat", "numeric"], ["lon", "numeric"]])
    print(sql_object.as_string(d.conn))
    c.execute(sql_object)
    # tupleNames = [("id", "serial"), ("redCARs", "VARCHAR(255)"), ("blueCars", "VARCHAR(255)")]
    # nullVals = ["redCARs", "blueCars"]
    # colNames = [x[0] for x in tupleNames]
    # sql_ob = s.colNames_string_query(s.tableName)
    # print(sql_ob.as_string(d.conn))
    # c.execute(sql_ob)
    # print(c.fetchall())
    # s.put_colNames_tableName_primary_key(colNames=colNames, tableName="Cats", prinmary_key="id")
    # print(s.insert_to_table(dataRow=["porsche", "junky"]))
    
    # version = c.fetchone()[0]
    # print(version)
    d.close()