from datetime import datetime

from coronado import TripleObject
from coronado.config import loadConfig
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.transaction import MatchingStatus
from coronado.transaction import ProcessorMIDType
from coronado.transaction import SERVICE_PATH
from coronado.transaction import Transaction
from coronado.transaction import TransactionType
from tests.test_address import _ADDRESS
from tests.test_cardaccount import generateKnownCardAccount
from tests.test_cardprog import generateKnownCardProgram
from tests.test_publisher import findOrGenerateKnownPublisher

import uuid

import pytest

import coronado.auth as auth


# *** globals ***

_config = loadConfig()
_auth = auth.Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
_publisher = findOrGenerateKnownPublisher()
_program = generateKnownCardProgram(_publisher.externalID)
_account = generateKnownCardAccount(_publisher.externalID, _program.externalID)
_transaction = None

Transaction.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# *** tests ***

def test_MatchingStatus():
    x = MatchingStatus.MATCHED

    assert isinstance(x, MatchingStatus)
    assert str(x) == 'MATCHED'
    assert str(x) == MatchingStatus.MATCHED.value


def test_ProcessorMIDType():
    x = ProcessorMIDType.VISA_VSID

    assert isinstance(x, ProcessorMIDType)
    assert str(x) == 'VISA_VSID'
    assert str(x) == ProcessorMIDType.VISA_VSID.value


def test_TransactionType():
    x = TransactionType.PURCHASE

    assert isinstance(x, TransactionType)
    assert str(x) == 'PURCHASE'
    assert str(x) == TransactionType.PURCHASE.value


def test_Transaction():
    t = Transaction()

    assert isinstance(t, Transaction)
    assert t.objID

    with pytest.raises(CallError):
        Transaction({ 'bogus': 'test'})
    with pytest.raises(CallError):
        Transaction(None)
    with pytest.raises(CallError):
        Transaction('bogus')


def test_Transaction_create():
    global _transaction

    # Happy path test with all required and non-required attrs:
    transaction = Transaction.create(
                    amount = 41.95,
                    extCardAccountID = _account.externalID,
                    extCardProgramID = _program.externalID,
                    debit = True,
                    description = 'Miscellaneous krap',
                    extTXID = 'tx-%s' % uuid.uuid4().hex,
                    merchantCategoryCode = '0744',
                    merchantAddress = _ADDRESS,
                    processorMID = uuid.uuid4().hex,
                    processorMIDType = ProcessorMIDType.VISA_VSID,
                    timestamp = datetime.now().replace(microsecond = 0).isoformat(),
                    transactionType = TransactionType.PURCHASE,
                    cardBIN = '425907',
                    cardLast4 = '3301',
                    currencyCode = 'USD',
                    extPublisherID = _publisher.externalID)

    assert isinstance(transaction, Transaction)
    assert transaction.objID
    assert transaction.amount == 41.95
    _transaction = transaction

    #Test CallError returned for invalid CardBINs and Last4s
    badBINs = ['', 'ABC', 'XXXXXX', '******']
    badLast4s = ['', 'ABCD', 'XXXX', '123', '*@*1']

    for badBIN in badBINs:
        with pytest.raises(CallError):
            transaction = Transaction.create(
                amount = 42.95,
                extCardAccountID = _account.externalID,
                extCardProgramID = _program.externalID,
                debit = True,
                description = 'Miscellaneous krap',
                extTXID = 'tx-%s' % uuid.uuid4().hex,
                merchantCategoryCode = '0744',
                merchantAddress = _ADDRESS,
                processorMID = uuid.uuid4().hex,
                processorMIDType = ProcessorMIDType.VISA_VSID,
                timestamp = '2021-12-01T01:59:59.000Z',
                transactionType = TransactionType.PURCHASE,
                cardBIN = badBIN,
                cardLast4 = '3301',
                currencyCode = 'USD',
                extPublisherID = _publisher.externalID)

    for badLast4 in badLast4s:
        with pytest.raises(CallError):
            transaction = Transaction.create(
                amount = 42.95,
                extCardAccountID = _account.externalID,
                extCardProgramID = _program.externalID,
                debit = True,
                description = 'Miscellaneous krap',
                extTXID = 'tx-%s' % uuid.uuid4().hex,
                merchantCategoryCode = '0744',
                merchantAddress = _ADDRESS,
                processorMID = uuid.uuid4().hex,
                processorMIDType = ProcessorMIDType.VISA_VSID,
                timestamp = '2021-12-01T01:59:59.000Z',
                transactionType = TransactionType.PURCHASE,
                cardBIN = '000000',
                cardLast4 = badLast4,
                currencyCode = 'USD',
                extPublisherID = _publisher.externalID)

    # Test with bogus duplicate external transaction
    with pytest.raises(InvalidPayloadError):
        Transaction.create(
            amount = 41.95,
            extCardAccountID = _account.externalID,
            extCardProgramID = _program.externalID,
            debit = True,
            description = 'Miscellaneous krap',
            extTXID = _transaction.externalID,
            merchantCategoryCode = '0744',
            merchantAddress = _ADDRESS,
            processorMID = uuid.uuid4().hex,
            processorMIDType = ProcessorMIDType.VISA_VSID,
            timestamp = '2021-12-01T01:59:59.000Z',
            transactionType = TransactionType.PURCHASE,
            cardBIN = '425907',
            cardLast4 = '3301',
            currencyCode = 'USD',
            extPublisherID = _publisher.externalID)


def test_Transaction_list():
    transactions = Transaction.list()

    if len(transactions):
        transaction = transactions[0]
        assert isinstance(transaction, TripleObject)
        assert transaction.objID

    transactions = Transaction.list(cardAccountExternalID = _account.externalID)
    assert transactions[0].matchingStatus in (MatchingStatus.NO_ACTIVE_OFFER,
                                              MatchingStatus.QUEUED)

    transactions = Transaction.list(cardProgramExternalID = _program.externalID)
    assert transactions[0].matchingStatus in (MatchingStatus.NO_ACTIVE_OFFER,
                                              MatchingStatus.QUEUED)

    # TODO:  Not implemented, no end dates known
#     transactions = Transaction.list(endDate = _program.externalID)
#     assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(matched = True)
    if len(transactions):
        assert transactions[0].matchingStatus == MatchingStatus.MATCHED

    transactions = Transaction.list(matched = False)
    if len(transactions):
        assert transactions[0].matchingStatus in (MatchingStatus.HISTORIC_TRANSACTION,
                                                  MatchingStatus.QUEUED)

    # TODO:  Not implemented, no start dates known
#     transactions = Transaction.list(startDate = _program.externalID)
#     assert transactions[0].matchingStatus == MatchingStatus.NO_ACTIVE_OFFER

    transactions = Transaction.list(transactionExternalID = _transaction.externalID)
    assert transactions[0].matchingStatus in (MatchingStatus.NO_ACTIVE_OFFER,
                                              MatchingStatus.QUEUED)


def test_Transaction_byID():
    result = Transaction.byID(_transaction.objID)
    assert isinstance(result, Transaction)

