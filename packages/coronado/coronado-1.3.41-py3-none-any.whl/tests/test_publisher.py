# vim: set fileencoding=utf-8:


from coronado.auth import Auth
from coronado.config import loadConfig
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.publisher import Publisher
from coronado.publisher import SERVICE_PATH
from tests.test_address import _ADDRESS

import uuid

import pytest


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

Publisher.initialize(_config['serviceURL'], SERVICE_PATH, _auth)

_publisher = None # Used for testing


# --- utility functions ---

def _generateTestPayload():
    addressNoComplete = _ADDRESS.asSnakeCaseDictionary()
    del addressNoComplete['complete']
    return {  # sn ::= snake case
        'address': addressNoComplete,
        'assumed_name': 'R2D2 Enterprises %s' % uuid.uuid4().hex,
        'external_id': uuid.uuid4().hex[-12:],
        'revenue_share': 1.5,
    }


# +++ tests +++

def test_Publisher_create():
    global _publisher

    pubSpec = _generateTestPayload()
    _publisher = Publisher.create(
                    assumedName = pubSpec['assumed_name'],
                    extPublisherID = pubSpec['external_id'],
                    address = pubSpec['address'],
                    revenueShare = pubSpec['revenue_share']
                )
    assert isinstance(_publisher, Publisher)
    assert _publisher.isCongruent()

    pubSpec['address']['country_code'] = 'ZZ'
    with pytest.raises(CallError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )

    pubSpec['address']['postal_code'] = ''
    with pytest.raises(InvalidPayloadError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )

    pubSpec['address']['postal_code'] = '123456789123456789'
    with pytest.raises(InvalidPayloadError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )

    pubSpec = _generateTestPayload()
    pubSpec['address']['country_code'] = 'USA'
    with pytest.raises(InvalidPayloadError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )

    pubSpec = _generateTestPayload()
    pubSpec['address']['street_address'] = ''
    with pytest.raises(InvalidPayloadError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )

    pubSpec = _generateTestPayload()
    pubSpec['external_id'] = _publisher.externalID
    with pytest.raises(InvalidPayloadError):
        Publisher.create(
            assumedName = pubSpec['assumed_name'],
            extPublisherID = pubSpec['external_id'],
            address = pubSpec['address'],
            revenueShare = pubSpec['revenue_share']
        )


def test_Publisher_list():
    results = Publisher.list()

    assert len(results)
    exists = False
    for publisher in results:
        if publisher.objID == _publisher.objID:
            exists = True
            break

    assert exists


def test_Publisher_byID():
    result = Publisher.byID(_publisher.objID)
    assert isinstance(result, Publisher)
    assert result.isCongruent()

    assert not Publisher.byID({ 'bogus': 'test'})
    assert not Publisher.byID(None)
    assert not Publisher.byID('bogus')


def test_Publisher_updateWith():
    address = _ADDRESS.asSnakeCaseDictionary()

    control = 'OOO Kukla'
    orgName = Publisher.byID(_publisher.objID).assumedName
    payload = { 'assumed_name' : control, 'address': address, }
    result = Publisher.updateWith(_publisher.objID, payload)
    assert result.assumedName == control

    # Reset:
    payload['assumed_name'] = orgName
    Publisher.updateWith(_publisher.objID, payload)


def test_Publisher_instanceByID():
    assert Publisher(_publisher.objID).assumedName == _publisher.assumedName


def findOrGenerateKnownPublisher():
    for publisher in Publisher.list():
        return publisher
    test_Publisher_create()
    return _publisher
