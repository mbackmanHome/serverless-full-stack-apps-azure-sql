import os
import pyodbc
#print(os.environ)
import json

#AZURE_CONN_STRING: str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:,1433;Database=bus-db;Uid=sql_admin;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


server = 'bus-server-mbackman.database.windows.net'
database = 'bus-db'
username = 'sql_admin'
password = 'Gtuv532d'   
driver= '{ODBC Driver 17 for SQL Server}'

#with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
 #   with conn.cursor() as cursor:
 #       cursor.execute("SELECT id, AgencyId FROM dbo.routes")
#        row = cursor.fetchone()
 #       while row:
#            print (str(row[0]) + " " + str(row[1]))
 #           row = cursor.fetchone()


#AZURE_CONN_STRING = 'DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password

AZURE_CONN_STRING: str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:bus-server-mbackman.database.windows.net,1433;Database=bus-db;Uid=sql_admin;Pwd=Gtuv532d;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn: str = pyodbc.connect(AZURE_CONN_STRING)
with conn.cursor() as cursor:
    cursor.execute(f"SELECT id, AgencyId FROM dbo.routes")
    #results = json.loads(cursor.fetchone()[0])
    #routes = [str(route['Id']) for route in results]

    results = cursor.fetchone()#[0]

    print(results)

