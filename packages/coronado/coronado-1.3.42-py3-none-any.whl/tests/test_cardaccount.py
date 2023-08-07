from coronado import TripleObject
from coronado.auth import Auth
from coronado.cardaccount import CardAccount
from coronado.cardaccount import CardAccountStatus
from coronado.cardaccount import SERVICE_PATH
from coronado.config import loadConfig
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.exceptions import NotImplementedError
from coronado.exceptions import UnprocessablePayload
from coronado.offer import CardholderOffer
from coronado.offer import CardholderOfferDetails
from coronado.offer import OfferType
from tests.test_cardprog import generateKnownCardProgram
from tests.test_publisher import findOrGenerateKnownPublisher

import uuid

import pytest



# +++ constants +++

VALID_TEST_COUNTRY_CODE = 'US'
KNOWN_OFFER_ID = '4862'
VALID_TEST_POSTAL_CODE = '15212'
VALID_TEST_POSTAL_CODE_LONG = '%s-1641' % VALID_TEST_POSTAL_CODE
KNOWN_OFFER_REQ_ACT_ID = '13487'
KNOWN_CARD_ACCOUNT = '31623'


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
_publisher = findOrGenerateKnownPublisher()
_program = generateKnownCardProgram(_publisher.externalID)
_account = None

CardAccount.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

def test_CardAccountStatus():
    x = CardAccountStatus('ENROLLED')

    assert x == CardAccountStatus.ENROLLED
    assert str(x) == 'ENROLLED'


def test_CardAccount_create():
    global _account
    spec = {
        'card_program_external_id': _program.externalID,
        'external_id': 'pnc-card-69-%s' % uuid.uuid4().hex,
        'publisher_external_id': _publisher.externalID,
        'status': str(CardAccountStatus.ENROLLED),
    }

    # Happy path
    account = CardAccount.create(
                extCardAccountID = spec['external_id'],
                extCardProgramID = spec['card_program_external_id'],
                defaultPostalCode = '94118',
                defaultCountryCode = 'US',
                extPublisherID = spec['publisher_external_id'],
                status = CardAccountStatus.ENROLLED
              )
    assert account.isCongruent()

    # No default postal code, country:
    spec['external_id'] = 'pnc-card-69-%s' % uuid.uuid4().hex
    account = CardAccount.create(
                extCardAccountID = spec['external_id'],
                extCardProgramID = spec['card_program_external_id'],
                extPublisherID = spec['publisher_external_id'],
                status = CardAccountStatus.ENROLLED
              )
    assert account.isCongruent()

    # No status:
    spec['external_id'] = 'pnc-card-69-%s' % uuid.uuid4().hex
    account = CardAccount.create(
                extCardAccountID = spec['external_id'],
                extCardProgramID = spec['card_program_external_id'],
                defaultPostalCode = '94118',
                defaultCountryCode = 'US',
                extPublisherID = spec['publisher_external_id'],
              )
    assert account.isCongruent()
    _account = account

    # Do not allow duplicate external card IDs
    with pytest.raises(InvalidPayloadError):
        CardAccount.create(
            extCardAccountID = account.externalID,
            extCardProgramID = spec['card_program_external_id'],
            extPublisherID = spec['publisher_external_id'],
            status = CardAccountStatus.ENROLLED
        )


def test_CardAccount_list():
    accounts = CardAccount.list()

    assert isinstance(accounts, list)

    if len(accounts):
        account = accounts[0]
        assert isinstance(account, TripleObject)
        assert account.isCongruent()

    accounts = CardAccount.list(pubExternalID = _publisher.externalID)
    assert accounts[0].status == CardAccountStatus.ENROLLED.value

    accounts = CardAccount.list(pubExternalID = _publisher.externalID, cardAccountExternalID = _account.externalID)
    assert accounts[0].status == CardAccountStatus.ENROLLED.value


def test_CardAccount_byID():
    result = CardAccount.byID(_account.objID)
    assert isinstance(result, CardAccount)

    assert not CardAccount.byID({ 'bogus': 'test'})
    assert not CardAccount.byID(None)
    assert not CardAccount.byID('bogus')


def test_CardAccount_byExternalID():
    acct = CardAccount.byExternalID(_account.externalID)
    control = CardAccount(_account.objID)
    assert acct.objID == control.objID
    assert acct.isCongruent()
    assert control.isCongruent()

    # Try a non-existent ID
    acct = CardAccount.byExternalID('boguzz')
    assert not acct


def test_CardAccount_updateWith():
    control = CardAccountStatus.NOT_ENROLLED
    payload = { 'status' : str(control), }
    obj  = CardAccount.updateWith(_account.objID, payload)
    assert obj.status == str(control)

    # Reset:
    payload['status'] = 'ENROLLED'
    CardAccount.updateWith(_account.objID, payload)


def test_CardAccount_findOffers():
    offers = _account.findOffers(
        filterType = OfferType.CARD_LINKED,
        latitude = 40.46,
        longitude = -79.92,
        pageOffset = 0,
        pageSize = 25,
        radius = 35000,
        textQuery = "italian food",
    )
    assert isinstance(offers[1], list)
    assert isinstance(offers[0], int)
    assert len(offers[1])
    assert offers[1][0].isCongruent()

    offers = _account.findOffers(
        countryCode = VALID_TEST_COUNTRY_CODE,
        postalCode = VALID_TEST_POSTAL_CODE,
        filterType = OfferType.CARD_LINKED,
        pageOffset = 0,
        pageSize = 25,
        radius = 35000,
        textQuery = "italian food",
    )
    assert isinstance(offers[1], list)
    assert isinstance(offers[0], int)
    assert len(offers[1])
    assert offers[1][0].isCongruent()

    offers = _account.findOffers(
        countryCode = VALID_TEST_COUNTRY_CODE,
        postalCode = VALID_TEST_POSTAL_CODE_LONG,
        filterType = OfferType.CARD_LINKED,
        pageOffset = 0,
        pageSize = 25,
        radius = 35000,
        textQuery = "italian food",
    )
    assert isinstance(offers[1], list)
    assert isinstance(offers[0], int)
    assert len(offers[1])
    assert offers[1][0].isCongruent()

    # Incomplete query - missing lat or long
    with pytest.raises(CallError):
        _account.findOffers(
            filterType = OfferType.CARD_LINKED,
            latitude = 40.46,
            pageOffset = 0,
            pageSize = 25,
            radius = 35000,
            textQuery = "italian food",
        )

    # Incomplete query - missing country or postal code
    with pytest.raises(CallError):
        _account.findOffers(
            postalCode = VALID_TEST_POSTAL_CODE_LONG,
            filterType = OfferType.CARD_LINKED,
            pageOffset = 0,
            pageSize = 25,
            radius = 35000,
            textQuery = "italian food",
        )

    # Invalid country test
    with pytest.raises(NotImplementedError):
        _account.findOffers(
            countryCode = 'RU',
            postalCode = '125009',
            filterType = OfferType.CARD_LINKED,
            pageOffset = 0,
            pageSize = 25,
            radius = 35000,
            textQuery = "italian food",
        )


def test_CardAccount_fetchOffer():
    offerViewerAccount = CardAccount(_account.objID)

    # Happy path test latitude, longitude:
    offerDetails = offerViewerAccount.fetchOffer(
            KNOWN_OFFER_ID,
            latitude = 49.46,
            longitude = -79.92,
            radius = 35000,
        )
    assert isinstance(offerDetails, CardholderOfferDetails)
    assert isinstance(offerDetails.offer, CardholderOffer)

    # Happy path test country, postalCode:
    offerDetails = offerViewerAccount.fetchOffer(
            KNOWN_OFFER_ID,
            countryCode = VALID_TEST_COUNTRY_CODE,
            postalCode = VALID_TEST_POSTAL_CODE_LONG,
            radius = 35000,
        )
    assert isinstance(offerDetails, CardholderOfferDetails)
    assert isinstance(offerDetails.offer, CardholderOffer)

    with pytest.raises(UnprocessablePayload):
        offerViewerAccount.fetchOffer(
            'BOGUs',
            countryCode = VALID_TEST_COUNTRY_CODE,
            postalCode = VALID_TEST_POSTAL_CODE_LONG,
            radius = 35000,
        )

    with pytest.raises(CallError):
        offerViewerAccount.fetchOffer(
                KNOWN_OFFER_ID,
                postalCode = VALID_TEST_POSTAL_CODE_LONG,
            )


def test_CardAccount_activateByID():
    
    activation = _account.activateByID(KNOWN_OFFER_REQ_ACT_ID)
    assert isinstance(activation, list)
    assert len(activation)

    # Invalid offerID provided
    with pytest.raises (InvalidPayloadError):
        _account.activateByID('bogus_ID')

    # No offerID provided
    with pytest.raises(TypeError):
        _account.activateByID()

@pytest.mark.skip('Not yet implemented in Triple.  Endpoint is live, but gives not implemented msg.')
def test_CardAccount_activateByCategory():
    # Activate all offers for this account matching a specific category
    # TODO: update for different category types once implemented - Triple only accepts FOOD 
    activations = _account.activateByCategory("FOOD")
    assert isinstance(activations, list)
    assert len(activations)

    # No category provided
    with pytest.raises(TypeError):
        _account.activateByCategory()


def test_CardAccount_offerActivations():
    # Have to use existing card account with a known activated offer to test.
    # Must already be in OpenSearch Offers Index
    account = CardAccount(KNOWN_CARD_ACCOUNT)
    activations = account.offerActivations()
    assert isinstance(activations, list)
    assert len(activations)


def generateKnownCardAccount(publisherExternalID = _publisher.externalID,
                                  cardProgramExternalID = _program.externalID):
    spec = {
        'card_program_external_id': cardProgramExternalID,
        'external_id': 'pnc-card-69-%s' % uuid.uuid4().hex,
        'publisher_external_id': publisherExternalID,
        'status': str(CardAccountStatus.ENROLLED),
    }
    return CardAccount.create(
                extCardAccountID = spec['external_id'],
                extCardProgramID = spec['card_program_external_id'],
                defaultPostalCode = '94118',
                defaultCountryCode = 'US',
                extPublisherID = spec['publisher_external_id'],
                status = spec['status']
           )


