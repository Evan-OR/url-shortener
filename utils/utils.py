import os 
from flask.wrappers import Request

def get_base_url(request:Request, shorten:bool=False):
    env_type = os.getenv('ENV_TYPE', os.environ.get('ENV_TYPE'))

    url = request.root_url if env_type == "DEBUG" else "https://www.lillink.net/"

    return url[12:] if shorten else url