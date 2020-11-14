# This is the file that will be used to build the database that is used with this program
from postquery import 

# This class will help with the building and adding of rows to the table
# It does this by adding constructing the string the will be used in the sql 
# query
class QueryStrings:
    def __init__(self, ):
        pass

    def create_table(self, tableName, primaryKey=None, Nullable=None, colNames=None, ):
        """
        This is the method that will be used to create a table.
        tableName:  This is a string of the table that you want to create
        primaryKey:  enter wich of the column names you would like to be a primary key if any.
        Nullable:   This expects a list of those colNames that can be Nullable, if empty all cols will be non_nullable.
        colNames:   This expects a list of tuples, with value 0 being the column name and the value 1 being the data type.

        Returns:    Will return the string used in the exucute function to make a table with the columns that you want

        """
        queryString = f"CREATE TABLE {tableName}, "
        # will now loop throught colNames and will add them to the query string
        if colNames:
            for name, dataType in colNames:
                queryString = queryString + "(" + name + " " + dataType
                if primaryKey == name:
                    queryString = queryString + " " + "PRIMARY KEY"
