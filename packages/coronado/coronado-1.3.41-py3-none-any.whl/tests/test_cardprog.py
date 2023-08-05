from coronado.auth import Auth
from coronado.cardprog import CardProgram
from coronado.cardprog import SERVICE_PATH
from coronado.config import loadConfig
from coronado.exceptions import InvalidPayloadError
from tests.test_publisher import findOrGenerateKnownPublisher

import uuid

import pytest


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
_program = None
_publisher = findOrGenerateKnownPublisher()


CardProgram.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

def test_CardProgram_create():
    global _program
    spec = {
        'card_bins': [ '425907', '511642', '486010', ],
        'default_country_code': 'US',
        'default_postal_code': '94123',
        'external_id': 'prog-%s' % uuid.uuid4().hex,
        'name': 'Mojito Rewards %s' % uuid.uuid4().hex,
        'program_currency': 'USD',
        'publisher_external_id': _publisher.externalID,
    }

    # Happy path:
    program = CardProgram.create(
                extCardProgramID = spec['external_id'],
                defaultPostalCode = spec['default_postal_code'],
                name = 'Mojito Rewards %s' % uuid.uuid4().hex,
                programCurrency = spec['program_currency'],
                cardBINs = spec['card_bins'],
                defaultCountryCode = spec['default_country_code'],
                extPublisherID = spec['publisher_external_id']
              )
    assert program.isCongruent()

    # No cardBINs optional argument
    program = CardProgram.create(
                extCardProgramID = 'prog-%s' % uuid.uuid4().hex,
                defaultPostalCode = spec['default_postal_code'],
                name = 'Mojito Rewards %s' % uuid.uuid4().hex,
                programCurrency = spec['program_currency'],
                defaultCountryCode = spec['default_country_code'],
                extPublisherID = spec['publisher_external_id']
              )
    assert program.isCongruent()

    # No defaultCountryCode optional argument
    program = CardProgram.create(
                extCardProgramID = 'prog-%s' % uuid.uuid4().hex,
                defaultPostalCode = spec['default_postal_code'],
                name = 'Mojito Rewards %s' % uuid.uuid4().hex,
                programCurrency = spec['program_currency'],
                cardBINs = spec['card_bins'],
                extPublisherID = spec['publisher_external_id']
              )
    assert program.isCongruent()

    _program = program # Now we have a global, well-known program for the next tests

    with pytest.raises(InvalidPayloadError):
        CardProgram.create(
            extCardProgramID = _program.externalID,
            defaultPostalCode = spec['default_postal_code'],
            name = 'Mojito Rewards %s' % uuid.uuid4().hex,
            programCurrency = spec['program_currency'],
            cardBINs = spec['card_bins'],
            defaultCountryCode = spec['default_country_code'],
            extPublisherID = spec['publisher_external_id']
        )

    with pytest.raises(InvalidPayloadError):
        CardProgram.create(
            extCardProgramID = '****',
            defaultPostalCode = spec['default_postal_code'],
            name = 'Mojito Rewards %s' % uuid.uuid4().hex,
            programCurrency = spec['program_currency'],
            cardBINs = spec['card_bins'],
            defaultCountryCode = spec['default_country_code'],
            extPublisherID = spec['publisher_external_id']
        )


def test_CardProgram_list():
    result = CardProgram.list()
    assert result[0].isCongruent()

    result = CardProgram.list(extCardProgramID = _program.externalID)

    assert len(result)
    assert result[0].isCongruent()


def test_CardProgram_byID():
    result = CardProgram.byID(_program.objID)
    assert isinstance(result, CardProgram)
    assert result.isCongruent()

    assert not CardProgram.byID({ 'bogus': 'test'})
    assert not CardProgram.byID(None)
    assert not CardProgram.byID('bogus')


def test_CardProgram_updateWith():
    control = 'OOO Kukla'
    orgName = CardProgram.byID(_program.objID).name
    payload = { 'name' : control, }
    result = CardProgram.updateWith(_program.objID, payload)
    assert result.name == control

    # Reset:
    payload['name'] = orgName
    CardProgram.updateWith(_program.objID, payload)


def generateKnownCardProgram(publisherExternalID = _publisher.externalID):
    spec = {
        'card_bins': [ '425907', '511642', '486010', ],
        'default_country_code': 'US',
        'default_postal_code': '94123',
        'external_id': 'prog-%s' % uuid.uuid4().hex,
        'name': 'Mojito Rewards %s' % uuid.uuid4().hex,
        'program_currency': 'USD',
        'publisher_external_id': publisherExternalID,
    }

    return CardProgram.create(
            extCardProgramID = spec['external_id'],
            defaultPostalCode = spec['default_postal_code'],
            name = spec['name'],
            programCurrency = spec['program_currency'],
            cardBINs = spec['card_bins'],
            defaultCountryCode = spec['default_country_code'],
            extPublisherID = spec['publisher_external_id']
    )

