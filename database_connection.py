import os
import mysql.connector
from dotenv import load_dotenv
from typing import Optional


def create_db_connection() -> Optional[mysql.connector.MySQLConnection]:
    load_dotenv()

    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    database = os.getenv('DATABASE')

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return None

def get_shorted_from_original(con:mysql.connector.MySQLConnection, url:str):
    cursor = con.cursor()
    cursor.execute("Select shortened_url from urls_info where original_url = %s", [url])
    result = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()

    return result[0][0]

def get_original_from_shortened(con:mysql.connector.MySQLConnection, url:str):
    cursor = con.cursor()
    cursor.execute("Select original_url from urls_info where shortened_url = %s", [url])
    result:dict = cursor.fetchall()

    # Close the cursor and the connection
    cursor.close()
    return result