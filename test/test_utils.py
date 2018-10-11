import os, pytest, sys

import hashlib
import hmac
import mock
from lanlytics_api_lib import utils

class TestUtils:
    def setup_method(self, _):
        os.environ['LANLYTICS_API_KEY'] = '123456testapikey'
        os.environ['LANLYTICS_API_SECRET_KEY'] = 'testapisecretkey123456'
        self.config = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials')

    def test_get_credentials(self):
        credentials = utils.get_credentials()
        assert(None not in credentials)

    @mock.patch('lanlytics_api.lib.utils.load_config', return_value=('key', 'secret'))
    def test_get_credentials_config(self, mock_load_config):
        del os.environ['LANLYTICS_API_KEY']
        del os.environ['LANLYTICS_API_SECRET_KEY']
        api_key, api_secret_key = utils.get_credentials()
        assert(api_key == 'key')
        assert(api_secret_key == 'secret')

    @mock.patch('lanlytics_api_lib.utils.load_config', side_effect=FileNotFoundError('File not found'))
    def test_get_credentials_config(self, mock_load_config):
        del os.environ['LANLYTICS_API_KEY']
        del os.environ['LANLYTICS_API_SECRET_KEY']
        api_key, api_secret_key = utils.get_credentials()
        assert(api_key == None)
        assert(api_secret_key == None)

    def test_load_config(self):
        api_key, api_secret_key = utils.load_config(config_file=self.config)
        assert(api_key == '123456testapikey')
        assert(api_secret_key == 'testapisecretkey123456')

    def test_load_config_not_found(self):
        with pytest.raises(FileNotFoundError):
            utils.load_config('no_config')

    def test_sign_request_payload(self):
        payload = 'foo'
        api_key, hashed_payload = utils.sign_request_payload(payload)
        assert(api_key == os.environ.get('LANLYTICS_API_KEY'))
        assert(hashed_payload == hmac.new(os.environ.get('LANLYTICS_API_SECRET_KEY').encode(),
                                          payload.encode(), hashlib.sha256).hexdigest())
