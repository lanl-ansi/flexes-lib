import hashlib
import hmac
import os
from configparser import ConfigParser

def has_credentials(credentials):
    '''Check if user has API credentials configured in environment.

    Args:
        credentials (tuple): A tuple containing (api_key, api_secret_key)

    Returns:
        bool
    '''
    return not None in credentials

def get_credentials():
    '''Retrieve user API credentials. Check environment variables first, then
        a configuration file if environment variables aren't set.

    Returns:
        tuple: User credentials (api_key, api_secret_key)
    '''
    api_key = os.environ.get('LANLYTICS_API_KEY')
    api_secret_key = os.environ.get('LANLYTICS_API_SECRET_KEY')

    credentials = (api_key, api_secret_key)

    if has_credentials(credentials):
        return credentials
    else:
        try:
            return load_config()
        except FileNotFoundError:
            return None, None


def load_config(config_file='~/.lanlytics/credentials'):
    '''Load user API credentials from file

    Args:
        config_file (str): Path to configuration file, default ~/.lanlytics/credentials

    Returns:
        tuple: User credentials (api_key, api_secret_key)
    '''
    if '~' in config_file:
        config_file = os.path.expanduser(config_file)

    if os.path.isfile(config_file):
        config = ConfigParser()
        config.read(config_file)
    else:
        raise FileNotFoundError('{} not found'.format(config_file))
    
    default = config['default']
    api_key = default.get('api_key')
    api_secret_key = default.get('api_secret_key')

    credentials = (api_key, api_secret_key)

    if has_credentials(credentials):
        return credentials


def sign_request_payload(payload):
    '''Sign API request payload with user keys

    Args:
        payload (str): Request payload

    Returns:
        tuple: (api_key, hashed_payload)
    '''
    credentials = get_credentials()

    if not has_credentials(credentials):
        raise ValueError('Invalid credentials')

    api_key = credentials[0]
    api_secret_key = credentials[1]

    hashed_payload = hmac.new(api_secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    return api_key, hashed_payload
