import os 
from flask.wrappers import Request

def get_base_url(request:Request):
    env_type = os.getenv('ENV_TYPE', os.environ.get('ENV_TYPE'))

    if env_type == "DEBUG":
        return request.root_url
    else:
        return "www.lillink.net/"