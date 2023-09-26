import os
import random
from urllib.parse import urlparse
import mysql.connector
import string
from dotenv import load_dotenv
from typing import Optional, Union

# TODO REWRITE THIS INTO AN OBJECT

def create_db_connection() -> Optional[mysql.connector.MySQLConnection]:
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

    # Load the .env file
    load_dotenv(env_path)

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

def get_original_from_shortened(con:mysql.connector.MySQLConnection, url:str) -> dict:
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT original_url, shortened_url FROM urls_info WHERE shortened_url = %s", [url])
    result = cursor.fetchone()

    cursor.close()
    if result:
        # If a matching record is found, return the original URL
        return result
    else:
        # If no matching record was found, return None or raise an exception, as needed
        raise ValueError('Shortened URL Not Found')

def shorten_url(con:mysql.connector.MySQLConnection, url:str) -> Union[None, dict]:
    # Check if valid url
    if not is_valid_url(url):
        raise ValueError('Invalid URL')

    # Return Link That Already Exists 
    exists, shortened_link = check_if_url_already_exists(con, url)

    if exists:
        return {
            "status": 200,
            "message": "Link Already Exists",
            "shortened": shortened_link
        }
    
    # Return New Generated New Link
    shortened_link = create_random_link(con)
    # Insert New Shortened URL
    post_new_url(con, url, shortened_link)

    return {
            "status": 200,
            "message": "New Link Created",
            "shortened": shortened_link
    }
    

def check_if_url_already_exists(con:mysql.connector.MySQLConnection, url:str)->bool:
    cursor = con.cursor()
    cursor.execute("SELECT shortened_url FROM urls_info where original_url = %s;", [url])
    result = cursor.fetchone()

    if result:
        return True, result[0]
    else:
        return False, None


def create_random_link(con:mysql.connector.MySQLConnection)-> str:
    characters = list(string.digits + string.ascii_lowercase + string.ascii_uppercase)
    cursor = con.cursor()
    
    while True:
        random_link = ''.join(random.choice(characters) for _ in range(5))
        
        cursor.execute("SELECT 1 FROM urls_info WHERE shortened_url = %s;", [random_link])
        if cursor.fetchone() is None:
            # The random link doesn't exist in the database, so we can break out of the loop.
            break
    
    return random_link

def post_new_url(con:mysql.connector.MySQLConnection, url:str, shortened_link:str):
    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO urls_info (original_url, shortened_url) VALUES (%s, %s);", [url, shortened_link])
        con.commit()
    except mysql.connector.Error as e:
        print(f"Error inserting data into the database: {e}")
        con.rollback() 
        raise ValueError('Couldn\' post new database record')
    finally:
        cursor.close()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
