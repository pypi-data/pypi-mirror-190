# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.auth import EXPIRATION_OFFSET
from coronado.config import loadConfig

import json
import time



# +++ tests +++

_config = loadConfig()


def test_Auth():
    Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])


def test_Auth_expired_token():
    a = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
    oldToken = a.token
    time.sleep(2)
    newToken = a.token
    assert oldToken == newToken

    b = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'], expirationOffset = EXPIRATION_OFFSET)
    oldToken = b._token
    assert oldToken != b.token


def test_Auth_accessToken():
    a = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
    control = json.loads(a.tokenPayload)['access_token']

    assert a.token == control


def test_Auth_tokenType():
    a = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
    control = json.loads(a.tokenPayload)['token_type']

    assert a.tokenType == control


def test_Auth_info():
    info = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret']).info
    assert info['tokenIssuerID']
    assert 'issuingServer' in info

