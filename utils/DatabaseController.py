import os
import random
from urllib.parse import urlparse
import mysql.connector
from mysql.connector.cursor import MySQLCursorDict
import mysql.connector.pooling
import string
from dotenv import load_dotenv
from typing import Optional, Union, Any


class DatabaseController():
    """
    A class for managing database operations related to URL shortening.

    Attributes:
        connection_pool (mysql.connector.pooling.MySQLConnectionPool): A connection pool for MySQL database.
        
    Methods:
        get_original_from_shortened(url: str) -> list[dict[str, Any]]:
            Retrieve the original URL associated with a shortened URL.

        shorten_url(url: str) -> Union[None, dict]:
            Shorten a URL and store it in the database, or return an existing shortened URL.

    Note:
        This class assumes that you have a MySQL database set up and configured with the necessary tables.

    """

    def __init__(self) -> None:
        self._initialize()

    def _initialize(self) -> Optional[mysql.connector.pooling.MySQLConnectionPool]:
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

        # Load the .env file
        load_dotenv(env_path)

        host, user, password, database = self._get_database_info()

        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name='my_pool',
                pool_size=5,
                pool_reset_session=True,
                host=host,
                user=user,
                password=password,
                database=database
            )
        except mysql.connector.Error as err:
            raise Exception(f"Failed to create connection pool: {err}")

    def get_original_from_shortened(self, url:str) -> list[dict[str, Any]]:
        connection = self.connection_pool.get_connection()
        cursor:MySQLCursorDict = connection.cursor(dictionary=True)

        cursor.execute("SELECT original_url, shortened_url FROM urls_info WHERE shortened_url = %s", [url])
        record = cursor.fetchone()

        cursor.close()
        connection.close()

        return record
    
    def shorten_url(self, url:str) -> Union[None, dict]:
        # Check if valid url
        if not self._is_valid_url(url):
            raise ValueError('Invalid URL')

        # Return Link That Already Exists 
        exists, shortened_link = self._url_already_exists(url)

        if exists:
            return {
                "status": 200,
                "message": "Link Already Exists",
                "shortened": shortened_link
            }
        
        # Return New Generated New Link
        shortened_link = self._create_unique_code()
        # Insert New Shortened URL
        self._add_new_link_to_database(url, shortened_link)

        return {
                "status": 200,
                "message": "New Link Created",
                "shortened": shortened_link
        }
    
    def _is_valid_url(self, url:str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    def _url_already_exists(self, url:str) -> tuple[bool, str]:
        connection = self.connection_pool.get_connection()
        cursor:MySQLCursorDict = connection.cursor(dictionary=True)

        cursor.execute("SELECT shortened_url FROM urls_info where original_url = %s;", [url])
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return True, result.get("shortened_url")
        else:
            return False, ""
        
    def _create_unique_code(self)-> str:
        connection = self.connection_pool.get_connection()
        cursor:MySQLCursorDict = connection.cursor(dictionary=True)

        characters = list(string.digits + string.ascii_lowercase + string.ascii_uppercase)
        
        while True:
            code = ''.join(random.choice(characters) for _ in range(5))
            
            cursor.execute("SELECT 1 FROM urls_info WHERE shortened_url = %s;", [code])
            if cursor.fetchone() is None:
                # The random link doesn't exist in the database, so we can break out of the loop.
                break
        
        cursor.close()
        connection.close()
        return code
    
    def _add_new_link_to_database(self, url:str, shortened_link:str):
        try:
            connection = self.connection_pool.get_connection()
            cursor:MySQLCursorDict = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO urls_info (original_url, shortened_url) VALUES (%s, %s);", [url, shortened_link])
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Error inserting data into the database: {e}")
            connection.rollback() 
            raise ValueError('Couldn\'t post new database record')
        finally:
            cursor.close()
            connection.close()

    def _get_database_info(self):
        # Try get variables from .env file first then try get details from environment.
        host = os.getenv('HOST', os.environ.get('HOST'))
        user = os.getenv('USER', os.environ.get('USER'))
        password = os.getenv('PASSWORD', os.environ.get('PASSWORD'))
        database = os.getenv('DATABASE', os.environ.get('DATABASE'))

        return host, user, password, database