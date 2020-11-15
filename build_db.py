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
        queryString = f"CREATE TABLE [IF NOT EXISTS] {tableName} ("
        # will now loop throught colNames and will add them to the query string
        if colNames:
            for i in range(len(colNames)):
                queryString = queryString +  colNames[i][0] + " " + colNames[i][1]
                if primaryKey == colNames[i][0]:
                    queryString = queryString + " " + "PRIMARY KEY"
                if colNames[i][0] not in Nullable:
                    queryString = queryString + " NOT NULL"
                if i < len(colNames)-1:
                    queryString =  queryString + ", "
        queryString = queryString + ")"
        return queryString


    def insert_to_table(self, tableName, dataRow, colNames):
        """
        This function will make the string which then can be used to inert a single row in 
        a postgresql database

        dataRow will be a list or tuple of values for the row
        """
        queryString = f"INSERT INTO {tableName} VALUES "
        # building the Values list
        valueString = ""
        # looping 
        for value in dataRow:


    def colNames_string(self):
        # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'some_table';
        """
        This function will return only the first
        part of the column names query so that you can get the column names

        Will return "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "
        """
        return "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "



if __name__ == "__main__":
    s = QueryStrings()
    tupleNames = [("id", "serial"), ("redCARs", "VARCHAR(255)"), ("blueCars", "VARCHAR(255)")]
    nullVals = ["redCARs", "blueCars"]

    
    print(s.create_table(tableName="cars", primaryKey="id", colNames=tupleNames, Nullable=nullVals))
