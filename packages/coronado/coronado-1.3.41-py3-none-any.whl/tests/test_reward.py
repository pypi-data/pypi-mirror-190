# vim: set fileencoding=utf-8:


from coronado import TripleObject
from coronado.auth import Auth
from coronado.config import loadConfig
from coronado.daterange import DateRange
from coronado.exceptions import CallError
from coronado.exceptions import UnprocessablePayload
from coronado.reward import Reward
from coronado.reward import RewardStatus
from coronado.reward import RewardType
from coronado.reward import SERVICE_PATH
from tests.test_cardaccount import generateKnownCardAccount
from tests.test_cardprog import generateKnownCardProgram, findOrGenerateKnownPublisher

import pytest


# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])

Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)

_reward = None

_publisher = findOrGenerateKnownPublisher()
_program = generateKnownCardProgram(_publisher.externalID)
_account = generateKnownCardAccount(_publisher.externalID, _program.externalID)
_transaction = None

# *** tests ***

def test_RewardType():
    reward = RewardType('FIXED')
    assert reward == RewardType.FIXED


def test_Reward_list():
    rewards = Reward.list()
    #assert len(rewards) > 0
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID


@pytest.mark.parametrize(
    "status", [
        RewardStatus.DENIED_BY_MERCHANT,
        RewardStatus.DISTRIBUTED_TO_CARDHOLDER,
        RewardStatus.DISTRIBUTED_TO_PUBLISHER,
        RewardStatus.PENDING_MERCHANT_APPROVAL,
        RewardStatus.PENDING_MERCHANT_FUNDING,
        RewardStatus.PENDING_REVIEW,
        RewardStatus.PENDING_TRANSFER_TO_PUBLISHER,
        # RewardStatus.REJECTED,
    ]
)
def test_Reward_list_with_status(status: RewardStatus) -> None:
    rewards = Reward.list(status = status)
    assert isinstance(rewards, list)
    if len(rewards):
        reward = rewards[0]
        assert isinstance(reward, TripleObject)
        assert reward.transactionID


def test_Reward_approve():
    approvedCount = len(Reward.list(status = RewardStatus.PENDING_MERCHANT_FUNDING))
    #TODO: process for having rewards in the DB with PENDING_MERCHANT_APPROVAL status
    #If there are no PENDING, can't approve them.  This skips the test if
    #no rewards with required status
    if len(Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)):
        reward = Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)[0]
        result = Reward.approve(reward.transactionID, reward.offerID)
        assert result
        assert len(Reward.list(status = RewardStatus.PENDING_MERCHANT_FUNDING)) == approvedCount+1

        with pytest.raises(UnprocessablePayload):
            Reward.approve(reward.transactionID, reward.offerID) # already approved

        with pytest.raises(UnprocessablePayload):
            Reward.approve('bogus-transaction', reward.offerID)

        with pytest.raises(UnprocessablePayload):
            Reward.approve(reward.transactionID, 'bogus-offer-id')


def test_Reward_deny():
    deniedCount = len(Reward.list(status = RewardStatus.DENIED_BY_MERCHANT))
    #TODO: process for having rewards in the DB with PENDING_MERCHANT_APPROVAL status
    #If there are no PENDING, can't deny them.  This skips the test if no rewards
    #with required status
    if len(Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)):
        reward = Reward.list(status = RewardStatus.PENDING_MERCHANT_APPROVAL)[0]
        result = Reward.deny(reward.transactionID, reward.offerID, notes = 'The cardholder wears ugly shoes')
        assert result
        assert len(Reward.list(status = RewardStatus.DENIED_BY_MERCHANT)) == deniedCount+1

        with pytest.raises(UnprocessablePayload):
            Reward.deny(reward.transactionID, reward.offerID, notes = "NOOP - this code shouldn't work") # already denied

        with pytest.raises(UnprocessablePayload):
            Reward.deny('bogus-transaction', reward.offerID, notes = "NOOP - this code shouldn't work")

        with pytest.raises(UnprocessablePayload):
            Reward.deny(reward.transactionID, 'bogus-offer-id', notes = "NOOP - this code shouldn't work")

        with pytest.raises(CallError):
            Reward.deny(reward.transactionID, reward.offerID, notes = '')

        with pytest.raises(CallError):
            Reward.deny(reward.transactionID, reward.offerID, notes = None)


def test_Reward_updateStatus():
    # TODO: Currently only testing happy path.
    #  Add fail cases and additional client impersonations
    reviewCount = len(Reward.list(status=RewardStatus.PENDING_REVIEW))
    approvedCount = len(Reward.list(status=RewardStatus.PENDING_MERCHANT_FUNDING))
    deniedCount = len(Reward.list(status=RewardStatus.DENIED_BY_MERCHANT))
    reward = Reward.list(status=RewardStatus.DENIED_BY_MERCHANT)[0]

    # Switch a reward from DENIED_BY_MERCHANT to PENDING_REVIEW
    result = Reward.updateStatus(transactionID=reward.transactionID, offerID=reward.offerID, status='PENDING_REVIEW')
    assert result
    # Validate there is an additional PENDING_REVIEW reward now
    assert len(Reward.list(status=RewardStatus.DENIED_BY_MERCHANT)) == deniedCount-1
    assert len(Reward.list(status=RewardStatus.PENDING_REVIEW)) == reviewCount+1

    # Switch a reward from PENDING_REVIEW to PENDING_MERCHANT_FUNDING
    result = Reward.updateStatus(transactionID=reward.transactionID, offerID=reward.offerID, status='PENDING_MERCHANT_FUNDING')
    assert result
    # Validate there is an additional PENDING_MERCHANT_FUNDING reward now
    assert len(Reward.list(status = RewardStatus.PENDING_REVIEW)) == reviewCount
    assert len(Reward.list(status=RewardStatus.PENDING_MERCHANT_FUNDING)) == approvedCount+1

    # Change the reward status back to DENIED
    result = Reward.updateStatus(transactionID=reward.transactionID, offerID=reward.offerID, status='DENIED_BY_MERCHANT')
    assert result
    assert len(Reward.list(status=RewardStatus.DENIED_BY_MERCHANT)) == deniedCount
    assert len(Reward.list(status=RewardStatus.PENDING_MERCHANT_FUNDING)) == approvedCount


@pytest.mark.skip('Skip for now.  Requires switch to Publisher client')
def test_Reward_aggregateByPublisher():

    # Test client ==  CONTENT_PROVIDER and valid extPublisherID:
    rewards = Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME, extPublisherID = _publisher.externalID)
    assert rewards
    assert 'https' in rewards.url

    # Test client == CONTENT_PROVIDER, extPublisherID omitted
    with pytest.raises(UnprocessablePayload):
        Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME)

    #Test client == CONTENT_PROVIDER and invalid extPublisherID:
    with pytest.raises(UnprocessablePayload):
        Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME, extPublisherID='Fail Test')

    #Test invalid date range provided

    #Switch to PUBLISHER client
    #TODO: reactivate switch to publisher if deemed correct method for testing this functionality
    #Reward.initialize(_config['serviceURL'], SERVICE_PATH, _authpub)
    # Test client ==  PUBLISHER and valid extPublisherID:
    rewards = Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME, extPublisherID = _publisher.externalID)
    assert rewards
    assert 'https' in rewards.url

    # Test client ==  PUBLISHER and omit extPublisherID:
    rewards = Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME)
    assert rewards
    assert 'https' in rewards.url

# TODO:  MERL-1253
    #assert isinstance(rewards.expiresAt, int)

# TODO:  MERL-1254
#     rewards = Reward.aggregateByPublisher(dateRangeTemplate = DateRange.LIFETIME)
#     assert rewards
#     assert 'https' in rewards.url
    # assert isinstance(rewards.expiresAt, int)


@pytest.mark.skip('Skip for now.  Requires switch to Publisher client')
def test_Reward_aggregateByCardProgram():
    # Test client == CONTENT_PROVIDER
    Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    rewards = Reward.aggregateByCardProgram(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardProgramID = _program.externalID,
        extPublisherID = _publisher.externalID,
        )
    assert rewards
    assert 'https' in rewards.url

    # Test client == CONTENT_PROVIDER, no extPublisher provided
    with pytest.raises(UnprocessablePayload):
        rewards = Reward.aggregateByCardProgram(
            dateRangeTemplate = DateRange.LIFETIME,
            extCardProgramID = _program.externalID,
            )

    # Test client == CONTENT_PROVIDER, no dateRange provided
    # Should this be a TypeError?
    with pytest.raises(TypeError):
        rewards = Reward.aggregateByCardProgram(
            extCardProgramID = _program.externalID,
            extPublisherID = _publisher.externalID,
            )

    # Test client == PUBLISHER
    #TODO: reactivate switch to publisher if deemed correct method for testing this functionality
    #Reward.initialize(_config['serviceURL'], SERVICE_PATH, _authpub)
    rewards = Reward.aggregateByCardProgram(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardProgramID = _program.externalID,
        extPublisherID = _publisher.externalID,
        )
    assert rewards
    assert 'https' in rewards.url

    # Test client == PUBLISHER, extPublisherID not requred
    rewards = Reward.aggregateByCardProgram(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardProgramID = _program.externalID,
        )
    assert rewards
    assert 'https' in rewards.url

    # Test client == PUBLISHER, no extCardProgram provided
    with pytest.raises(TypeError):
        rewards = Reward.aggregateByCardProgram(
            dateRangeTemplate = DateRange.LIFETIME,
            extPublisherID = _publisher.externalID,
        )

@pytest.mark.skip('Skip for now.  Requires switch to publisher client.')
def test_Reward_aggregateByCardAccount():
    #Test client == CONTENT_PROVIDER
    Reward.initialize(_config['serviceURL'], SERVICE_PATH, _auth)
    rewards = Reward.aggregateByCardAccount(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardAccountID = _account.external_ID,
        extCardProgramID = _program.externalID,
        extPublisherID = _publisher.externalID)
    assert rewards
    assert isinstance(rewards,TripleObject)

    #Test client == CONTENT_PROVIDER, no extPublisherID provided
    with pytest.raises(UnprocessablePayload):
        Reward.aggregateByCardAccount(
            dateRangeTemplate = DateRange.LIFETIME,
            extCardAccountID = _account.externalID,
            extCardProgramID = _program.externalID,
            )

    #Switch to Publisher Client
    #TODO: reactivate switch to publisher if deemed correct method for testing this functionality
    #Reward.initialize(_config['serviceURL'], SERVICE_PATH, _authpub)
    #Test client == PUBLISHER
    rewards = Reward.aggregateByCardAccount(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardAccountID = _account.externalID,
        extCardProgramID = _program.externalID,
        extPublisherID = _publisher.externalID,
        )
    assert rewards

    #Test client == PUBLISHER extPublisherID not required
    rewards = Reward.aggregateByCardAccount(
        dateRangeTemplate = DateRange.LIFETIME,
        extCardAccountID = _account.externalID,
        extCardProgramID = _program.externalID,
        )
    assert rewards

    #Test client == PUBLISHER no extCardProgram provided
    with pytest.raises(TypeError):
        Reward.aggregateByCardAccount(
            dateRangeTemplate = DateRange.LIFETIME,
            extCardAccountID = _account.externalID,
            )
