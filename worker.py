# This is the file that will be used to have the code that is used to work with the 
# postgres database either local or remote


from settings import username, password, host, database
from psycopg2 import sql
import psycopg2
import os
from geo import GeoLocation

path_to_csv = os.path.join(os.path.realpath(__file__), "..", "radian_df.csv")

def create_staging(cursor, ):
    cursor.execute(
        """
            DROP TABLE IF EXISTS airb;
             CREATE TABLE airb (
            id      integer PRIMARY KEY,
            lat     numeric (8, 6),
            lon     numeric (8, 6),
            room_type  VARCHAR (255),
            price       integer,
            nin_nights integer
            
        )
        """
    )



def send_csv_psql(connection, csvfile, tableName):
    sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
    thefile = open(csvfile, 'r')
    table = tableName
    with connection.cursor() as cursor:
        cursor.execute("truncate " + table)
        cursor.copy_expert(sql=sql % table, file=thefile)
    
    cursor.close()

    return connection.commit()

	

def query(bounding_coord, loc :GeoLocation, connection, num_nights, room_type):
    """
    This is the function that will make the query string 

    """
    boolVal = "AND"
    if GeoLocation.meridian180WithinDistance(bounding_coord):
        boolVal = "OR"
    sql_lon =  sql.SQL("lon >= {lon_coord_1} {theBool} lon <={lon_coord_2}").format(
        lon_coord_1=sql.Literal(bounding_coord[0].rad_lon),
        theBool=sql.SQL(boolVal),
        lon_coord_2=sql.Literal(bounding_coord[1].rad_lon)
    )

    sql_lon_str = sql_lon.as_string(connection)
    #"acos(sin(?) * sin(Lat) + cos(?) * cos(Lat) * cos(Lon - ?)) <= ?");
    
    math_sql = sql.SQL("acos(sin({loc_lat_rad}) * sin(lat) + cos({loc_lat_rad}) * cos(lat) * cos(lon - ({loc_lon_rad}))) <= {dist_divide_radius}").format(
        loc_lat_rad=sql.SQL(str(loc.rad_lat)),
        loc_lon_rad=sql.SQL(str(loc.rad_lon)),
        dist_divide_radius=sql.SQL(str(loc.radius))
    )
    math_str = math_sql.as_string(connection)

    sql_ob1 = sql.SQL("SELECT price FROM airb WHERE lat >= {lat_coord_1} AND lat <= {lat_coord_2} AND {lon_val} AND {math_val} AND room_type = {room_type} AND nin_nights <= {nights}").format(
            lat_coord_1 = sql.Literal(bounding_coord[0].rad_lat), lat_coord_2= sql.Literal(bounding_coord[1].rad_lat),
            theBool = sql.SQL(boolVal),lon_val=sql.SQL(sql_lon_str),
            math_val=sql.SQL(math_str),
            room_type=sql.Literal(room_type),
            nights=sql.Literal(num_nights)
            )
    return sql_ob1


def return_avg_price(lat, lon, room_type, num_nights):
    """
    This function is to find the price average for those items that it pulls 
    from the query."""


if __name__ == "__main__":

    # getting the connection
    conn = psycopg2.connect(dbname=database, password=password, host=host, user=username)
    
    # # doing the staging the create table
    # with conn.cursor() as cursor:
    #     create_staging(cursor)

    # send_csv_psql(conn, path_to_csv, "airb")
    # # C:\Users\rich\Richard_python\Lambda\labs\resfeber_data\radian_df.csv   
    
    # Instaciating the GeoLocation class
    geoClass = GeoLocation.from_degrees(deg_lat=43.717869, deg_lon= -110.317117)

    print(f"The radius is : {geoClass.radius}")

    # getting the bound coord
    bounding = geoClass.bounding_locations(geoClass.dist_kilo, geoClass.EARTH_RADIUS)
    # passing into the function
    sql_ob = query(bounding_coord=bounding, loc=geoClass, connection=conn, num_nights=5, room_type='Private room')
    print(sql_ob.as_string(conn))
    #print(sql_ob.as_string(conn))
    curs = conn.cursor()
    curs.execute(sql_ob)

    res = curs.fetchall()
    
    print(res)
    print(f"the length of the results is {len(res)}")

    curs.close()
    conn.close()
    