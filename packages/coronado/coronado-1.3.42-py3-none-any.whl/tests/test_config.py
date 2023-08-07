from coronado.config import CONFIGURATION_PATH
from coronado.config import LOG_PATH
from coronado.config import _logInit
from coronado.config import emptyConfig
from coronado.config import envConfig
from coronado.config import loadConfig

import logging
import os


# +++ tests +++

# NB:  These tests don't use fixtures because they need to run against the
# actual service.  This may change in the future.

def test__logInit():
    config = { 'loglevel': 'INFO', }

    os.makedirs(LOG_PATH, exist_ok = True)
    logFileName = os.path.join(LOG_PATH, 'test-coronado.log')

    _logInit(config, logFileName)

    log = logging.getLogger(__name__)
    log.critical('Hello, world!')


def test_loadConfig():
    # Uses default file names, present in the file system:
    config = loadConfig()

    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config

    # Unit test only:
    testConfig = { 'clientID': 'someClientID4269', 'clientName': 'unitTest', }
    config = loadConfig(testConfig = testConfig)
    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config

    # Unit test only, validate the file name:
    testConfig = { 'clientID': 'someClientID4269', 'clientName': 'unitTest', }
    bogusFileName = 'whatever.json'
    config = loadConfig(fileName = bogusFileName, testConfig = testConfig)
    control = os.path.join(CONFIGURATION_PATH, bogusFileName)
    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config
    assert 'testFileName' in config
    assert config['testFileName'] == control

    # Test if environment configuration
    os.environ['CORONADO_SECRET'] = 'shhhhhh'
    config = loadConfig(fileName = bogusFileName)
    assert 'shhhhhh' == config['secret']
    del os.environ['CORONADO_SECRET']


def test_emptyConfig():
    config = emptyConfig()

    assert isinstance(config, dict)
    assert 'clientID' in config
    assert 'clientName' in config


def test_envConfig():
    os.environ['CORONADO_CLIENT_ID'] = 'someClient'
    os.environ['CORONADO_SECRET'] = 'shhhhhh'
    os.environ['CORONADO_SERVICE_URL'] = 'https://triple.rocks'
    os.environ['CORONADO_TOKEN_URL'] = 'https://triple.secret.shh'

    config = envConfig()
    assert 'clientID' in config
    assert 'shhhhhh' == config['secret']

    # Incomplete configuration, missing items are None:
    del os.environ['CORONADO_SECRET']
    config = envConfig()
    assert config['secret'] == None

