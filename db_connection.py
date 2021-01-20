import mysql.connector
from mysql.connector import Error
from flask import render_template
import json
def db_conn():
    try:
        connection = mysql.connector.connect(host='localhost',
                                              database='fruits',
                                              user='root',
                                              password='password')
        
                                 
        if connection.is_connected():
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)

def get_data(table_name):
    try:
        conn = db_conn()                                      
        if conn.is_connected():
            db_Info = conn.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = conn.cursor()
            cursor.execute("select * from " + table_name + ";")
            result = dict(cursor.fetchall())
            return render_template('result.html', result=result)     
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close() 


# if __name__ == "__main__":
#     print(get_data("vegetagles"))
