from copy import deepcopy

from coronado import TripleEnum
from coronado import TripleObject
from coronado.address import Address
from coronado.auth import Auth
from coronado.baseobjects import BASE_ADDRESS_DICT
from coronado.baseobjects import BASE_ADDRESS_JSON
from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.baseobjects import BASE_CARD_ACCOUNT_JSON
from coronado.baseobjects import BASE_CARD_PROGRAM_DICT
from coronado.baseobjects import BASE_CARD_PROGRAM_JSON
from coronado.baseobjects import BASE_MERCHANT_DICT
from coronado.baseobjects import BASE_MERCHANT_JSON
from coronado.baseobjects import BASE_PUBLISHER_DICT
from coronado.baseobjects import BASE_PUBLISHER_JSON
from coronado.cardaccount import CardAccount
from coronado.cardprog import CardProgram
from coronado.config import loadConfig
from coronado.exceptions import CallError
from coronado.exceptions import UnprocessablePayload
from coronado.merchant import Merchant
from coronado.publisher import Publisher

import pytest


# *** constants ***


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])


# --- tests ---

def _createAndAssertObject(klass, pJSON, pDict, testKey = None, controlKey = None):
    with pytest.raises(CallError):
        klass(42)

    x = klass(pJSON)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]

    x = klass(pDict)
    if testKey:
        assert x.__dict__[testKey] == pDict[controlKey]


def test_TripleObject():
    x = TripleObject(BASE_PUBLISHER_DICT)
    y = x.listAttributes()

    assert 'portfolioManagerID' in y.keys()

    z = Publisher(x)
    assert isinstance(z, Publisher)


def test_TripleObjectMissingAttrError() -> object:
    x = deepcopy(BASE_PUBLISHER_DICT)
    del(x['assumed_name'])

    try:
        Publisher(x)
    except CallError as e:
        assert str(e) == '{"tripleInfo": "attribute {\'assumedName\'} missing during instantiation", "errno": -1}'

    del(x['address'])
    with pytest.raises(CallError) as e:
        Publisher(x)
        assert str(e) == "attributes {'assumedName', 'address'} missing during instantiation"


def test_APIObjectsInstantiation():
    _createAndAssertObject(Address, BASE_ADDRESS_JSON, BASE_ADDRESS_DICT, 'countryCode', 'country_code')
    _createAndAssertObject(CardAccount, BASE_CARD_ACCOUNT_JSON, BASE_CARD_ACCOUNT_DICT, 'objID', 'id')
    _createAndAssertObject(CardProgram, BASE_CARD_PROGRAM_JSON, BASE_CARD_PROGRAM_DICT, 'publisherID', 'publisher_id')
    _createAndAssertObject(Merchant, BASE_MERCHANT_JSON, BASE_MERCHANT_DICT, 'externalID', 'external_id')
    _createAndAssertObject(Publisher, BASE_PUBLISHER_JSON, BASE_PUBLISHER_DICT, 'assumedName', 'assumed_name')


def test_TripleObject_classVariables():
    # Uninitialized
    assert Address._serviceURL == CardAccount._serviceURL
    assert Address._auth == CardAccount._auth

    # Initialize one of them
    Address._serviceURL = 'https://example.com'
    Address._auth = { 'bogus': '42', }

    assert Address._serviceURL != CardAccount._serviceURL
    assert Address._auth != CardAccount._auth


def test_TripleObject_initialize():
    control = 'BOGUS'
    TripleObject.initialize(_config['serviceURL'], control, _auth)

    assert TripleObject._serviceURL == _config['serviceURL']
    assert TripleObject._servicePath == control
    assert 'python-coronado' in TripleObject.headers['User-Agent']

    badPath = '/%s' % control
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control

    badPath = '%s/' % control
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control

    badPath = '/%s/' % control
    TripleObject.initialize(_config['serviceURL'], badPath, _auth)
    assert TripleObject._servicePath == control


def test_TripleObject_headers():
    # Must follow test_TripleObject_initialize() to work; it uses
    # the class variables.

    h = TripleObject.headers

    assert isinstance(h, dict)
    assert 'Authorization' in h
    assert 'User-Agent' in h


def test_TripleObject_requiredAttributes():
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]

    s = Synthetic({ 'alpha': 42, 'theta_meta': 69, 'beta': 99, })
    assert 'thetaMeta' in s.listAttributes()

    with pytest.raises(CallError):
        Synthetic({ 'alpha': 42, 'theta_meta': 69, })


def test_TripleObject___str__():
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]

    s = Synthetic({ 'alpha': 42, 'theta_meta': 69, 'beta': 99, })
    assert str(s)


def test_TripleObject_isComplete():
    # Complete object validation
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]
        allAttributes = { 'alpha': int, 'gamma': int, 'beta': int, }

    s = Synthetic({ 'alpha': 42, 'gamma': 69, 'beta': 99, })
    assert s.isComplete()

    # Incomplete object:
    s = Synthetic({ 'alpha': 42, 'beta': 99, })
    assert not s.isComplete()


def test_TripleObject_extraneusAttributes():
    # Complete object
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]
        allAttributes = { 'alpha': int, 'gamma': int, 'beta': int, }

    s = Synthetic({ 'alpha': 42, 'gamma': 69, 'beta': 99, })
    assert not s.extraneousAttributes()

    # Extraneous attributes in Triple API:
    s = Synthetic({ 'alpha': 42, 'gamma': 69, 'beta': 99, 'theta': 0, })
    assert s.extraneousAttributes()


def test_TripleObject_isCongruent():
    # Complete object
    class Synthetic(TripleObject):
        requiredAttributes = [ 'alpha', 'beta', ]
        allAttributes = { 'alpha': int, 'gamma': int, 'beta': int, }

    s = Synthetic({ 'alpha': 42, 'gamma': 69, 'beta': 99, })
    assert s.isCongruent()

    # Incomplete object:
    s = Synthetic({ 'alpha': 42, 'beta': 99, })
    with pytest.raises(UnprocessablePayload):
        s.isCongruent()

    # Extraneous attributes in Triple API:
    s = Synthetic({ 'alpha': 42, 'gamma': 69, 'beta': 99, 'theta': 0, })
    with pytest.raises(UnprocessablePayload):
        s.isCongruent()


def test_TripleEnum():
    class Bogus(TripleEnum):
        XX = 42
        YY = 69

    x = Bogus.XX

    assert x == Bogus.XX
    assert x.value == 42
    assert str(x) == '42'


test_TripleObject_isCongruent()

