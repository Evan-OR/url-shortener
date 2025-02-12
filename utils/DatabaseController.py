import os
import random
from urllib.parse import urlparse
import string
from typing import Union, Any

from pymongo import MongoClient


class DatabaseController:

    def __init__(self) -> None:
        MONGO_URL = os.getenv("MONGO_URL", os.environ.get("MONGO_URL"))
        DATABASE = os.getenv("DATABASE", os.environ.get("DATABASE"))
        COLLECTION = os.getenv("COLLECTION", os.environ.get("COLLECTION"))

        client = MongoClient(MONGO_URL)
        url_database = client.get_database(DATABASE)

        self.url_collection = url_database.get_collection(COLLECTION)

    def get_original_from_shortened(self, code: str):
        urlData = self.url_collection.find_one({"code": code})

        return urlData

    def shorten_url(self, url: str) -> Union[None, dict]:
        # Check if valid url
        if not self._is_valid_url(url):
            raise ValueError("Invalid URL")

        # Return Link That Already Exists
        exists, shortened_link = self._url_already_exists(url)

        if exists:
            return {
                "status": 200,
                "message": "Link Already Exists",
                "shortened": shortened_link,
            }

        # Return New Generated New Link
        code = self._create_unique_code()
        # Insert New Shortened URL
        self._add_new_link_to_database(url, code)

        return {
            "status": 200,
            "message": "New Link Created",
            "shortened": code,
        }

    def _is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def _url_already_exists(self, url: str) -> tuple[bool, str]:
        result = self.url_collection.find_one({"originalUrl": url})

        if result:
            return True, result["code"]
        else:
            return False, ""

    def _create_unique_code(self) -> str:
        characters = list(
            string.digits + string.ascii_lowercase + string.ascii_uppercase
        )

        while True:
            code = "".join(random.choice(characters) for _ in range(5))

            result = self.url_collection.find_one({"code": code})

            if result is None:
                break

        return code

    def _add_new_link_to_database(self, url: str, code: str):
        self.url_collection.insert_one({"originalUrl": url, "code": code})

    def _get_database_info(self):
        # get variables from .env file first then try get details from environment.
        host = os.getenv("HOST", os.environ.get("HOST"))
        user = os.getenv("USER", os.environ.get("USER"))
        password = os.getenv("PASSWORD", os.environ.get("PASSWORD"))
        database = os.getenv("DATABASE", os.environ.get("DATABASE"))

        return host, user, password, database
