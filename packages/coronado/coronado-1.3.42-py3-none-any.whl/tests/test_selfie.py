# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.auth import Auth
from coronado.config import loadConfig
from coronado.selfie import Selfie
from coronado.selfie import SERVICE_PATH
from coronado.selfie import main


# +++ tests +++

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
Selfie.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


def test_Selfie():
    result = Selfie.snapshot()

    assert isinstance(result, TripleObject)
    assert 'clientID' in result.__dict__


def test_Selfie_main():
    info = main(unitTest = True)
    assert isinstance(info, dict)
    assert 'clientID' in info

