import hashlib
import hmac
import os
from configparser import ConfigParser

def get_credentials():
    api_key = os.environ.get('LANLYTICS_API_KEY')
    api_secret_key = os.environ.get('LANLYTICS_API_SECRET_KEY')

    credentials = (api_key, api_secret_key)

    if not None in credentials:
        return credentials
    else:
        return load_config()


def load_config():
    config = ConfigParser()
    config.read('~/.lanlytics/credentials')
    
    default = config['default']
    api_key = default.get('api_key')
    api_secret_key = default.get('api_secret_key')

    credentials = (api_key, api_secret_key)

    if not None in credentials:
        return credentials


def sign_request_payload(payload):
    credentials = get_credentials()

    if credentials is None:
        raise ValueError('Invalid credentials')

    api_key = credentials[0]
    api_secret_key = credentials[1]

    hashed_payload = hmac.new(api_secret_key, msg=payload, hashlib.sha256).digest()

    return api_key, hashed_payload
