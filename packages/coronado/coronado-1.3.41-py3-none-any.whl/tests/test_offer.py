# vim: set fileencoding=utf-8:

from coronado import TripleObject
from coronado.auth import Auth
from coronado.config import loadConfig
from coronado.exceptions import CallError
from coronado.exceptions import InvalidPayloadError
from coronado.offer import MarketingFeeType
from coronado.offer import Offer
from coronado.offer import OfferCategory
from coronado.offer import OfferType
from coronado.offer import SERVICE_PATH
from tests.test_merchant import generateKnownMerchant

import pytest
import uuid

# *** globals ***

_config = loadConfig()
_auth = Auth(_config['tokenURL'], clientID = _config['clientID'], clientSecret = _config['secret'])
_merchant = generateKnownMerchant()
_offer = None

Offer.initialize(_config['serviceURL'], SERVICE_PATH, _auth)


# +++ tests +++

def test_MarketingFeeType():
    x = MarketingFeeType.PERCENTAGE

    assert isinstance(x, MarketingFeeType)
    assert str(x) == 'PERCENTAGE'
    assert str(x) == MarketingFeeType.PERCENTAGE.value



def test_OfferCatetory():
    x = OfferCategory.ENTERTAINMENT

    assert isinstance(x, OfferCategory)
    assert str(x) == 'ENTERTAINMENT'
    assert str(x) == OfferCategory.ENTERTAINMENT.value


def test_OfferType():
    x = OfferType.AFFILIATE

    assert x == OfferType.AFFILIATE
    assert str(x) == 'AFFILIATE'
    assert str(x) == OfferType.AFFILIATE.value


def test_Offer_create():
    global _offer

    spec = {
        'activation_required': False,
        'currency_code': 'USD',
        'effective_date': '2022-12-01',
        'external_id': 'offer-%s' % uuid.uuid4().hex,
        'headline': 'Get 5 Percent back on this Test Offer',
        'marketing_fee_type': 'PERCENTAGE',
        'minimum_spend': 0,
        'reward_type': 'PERCENTAGE',
        'offer_type': 'CARD_LINKED',
        'activation_duration_in_days': None,
        'campaign_ends_on': None,
        'category': 'FOOD',
        'category_tags': 'Catering, Delivery Services, Grocery Stores, Restaurants',
        'description': 'Test Offer Description',
        'excluded_dates': None,
        'expiration_date': None,
        'marketing_fee_currency_code': None,
        'marketing_fee_rate': 1.0,
        'marketing_fee_value': None,
        'max_redemptions': None,
        'maximum_cumulative_reward': None,
        'maximum_reward_per_transaction': None,
        'merchant_categories': None,
        'merchant_external_id': _merchant.externalID,
        'merchant_website': None,
        'mode': 'IN_PERSON',
        'reward_rate': 0.0,
        'reward_value': None,
        'terms': None,
        'valid_day_parts': None,
    }

    offer = Offer.create(
            activationRequired = spec['activation_required'],
            currencyCode = spec['currency_code'],
            effectiveDate = spec['effective_date'],
            externalID = spec['external_id'],
            headline = spec['headline'],
            marketingFeeType = spec['marketing_fee_type'],
            minimumSpend = spec['minimum_spend'],
            rewardType = spec['reward_type'],
            offerType = spec['offer_type'],
            activationDurationInDays = spec['activation_duration_in_days'],
            campaignEndsOn = spec['campaign_ends_on'],
            category = spec['category'],
            categoryTags = spec['category_tags'],
            description = spec['description'],
            excludedDates = spec['excluded_dates'],
            expirationDate = spec['expiration_date'],
            marketingFeeCurrencyCode = spec['marketing_fee_currency_code'],
            marketingFeeRate = spec['marketing_fee_rate'],
            marketingFeeValue = spec['marketing_fee_value'],
            maxRedemptions = spec['max_redemptions'],
            maximumCumulativeReward = spec['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec['maximum_reward_per_transaction'],
            merchantCategories = spec['merchant_categories'],
            merchantExternalID = spec['merchant_external_id'],
            merchantWebsite = spec['merchant_website'],
            mode = spec['mode'],
            rewardRate = spec['reward_rate'],
            rewardValue = spec['reward_value'],
            terms = spec['terms'],
            validDayParts = spec['valid_day_parts'],
        )

    assert offer.isCongruent()
    assert isinstance(offer, Offer)
    _offer = offer

    # Do not allow duplicate offer IDs
    with pytest.raises(InvalidPayloadError):
        Offer.create(
            activationRequired = spec['activation_required'],
            currencyCode = spec['currency_code'],
            effectiveDate = spec['effective_date'],
            externalID = _offer.externalID,
            headline = spec['headline'],
            minimumSpend = spec['minimum_spend'],
            rewardType = spec['reward_type'],
            offerType = spec['offer_type'],
            activationDurationInDays = spec['activation_duration_in_days'],
            campaignEndsOn = spec['campaign_ends_on'],
            category = spec['category'],
            categoryTags = spec['category_tags'],
            description = spec['description'],
            excludedDates = spec['excluded_dates'],
            expirationDate = spec['expiration_date'],
            marketingFeeCurrencyCode = spec['marketing_fee_currency_code'],
            marketingFeeRate = spec['marketing_fee_rate'],
            marketingFeeType = spec['marketing_fee_type'],
            marketingFeeValue = spec['marketing_fee_value'],
            maxRedemptions = spec['max_redemptions'],
            maximumCumulativeReward = spec['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec['maximum_reward_per_transaction'],
            merchantCategories = spec['merchant_categories'],
            merchantExternalID = spec['merchant_external_id'],
            merchantWebsite = spec['merchant_website'],
            mode = spec['mode'],
            rewardRate = spec['reward_rate'],
            rewardValue = spec['reward_value'],
            terms = spec['terms'],
            validDayParts = spec['valid_day_parts'],
        )

    spec2 = {
        'activation_required': False,
        'currency_code': 'USD',
        'effective_date': '2022-12-01',
        'external_id': 'offer-%s' % uuid.uuid4().hex,
        'headline': 'Get 5 Percent back on this Test Offer',
        'marketing_fee_type': 'PERCENTAGE',
        'minimum_spend': 2,
        'reward_type': 'PERCENTAGE',
        'offer_type': 'CARD_LINKED',
        'activation_duration_in_days': 100,
        'campaign_ends_on': '2023-12-01',
        'category': 'FOOD',
        'category_tags': 'Catering, Delivery Services, Grocery Stores, Restaurants',
        'description': 'Test Offer Description',
        'excluded_dates': ['2023-01-10','2023-01-20'],
        'expiration_date': '2023-12-01',
        'marketing_fee_currency_code': 'USD',
        'marketing_fee_rate': 1.0,
        'marketing_fee_value': None,
        'max_redemptions': '5/1W',
        'maximum_cumulative_reward': '5/1W',
        'maximum_reward_per_transaction': 10,
        'merchant_categories': [
            {
                'merchant_category_code': 7998,
                'description': 'Aquariums, Dolphinariums, Seaquariums, and Zoos'
            }
            ],
        'merchant_external_id': _merchant.externalID,
        'merchant_website': 'https://randommerchantwebsite.bogus',
        'mode': 'IN_PERSON',
        'reward_rate': 0.0,
        'reward_value': None,
        'terms': 'Terms and Conditions',
        'valid_day_parts': None,
    }

    offer = Offer.create(
            activationRequired = spec2['activation_required'],
            currencyCode = spec2['currency_code'],
            effectiveDate = spec2['effective_date'],
            externalID = spec2['external_id'],
            headline = spec2['headline'],
            marketingFeeType = spec2['marketing_fee_type'],
            minimumSpend = spec2['minimum_spend'],
            rewardType = spec2['reward_type'],
            offerType = spec2['offer_type'],
            activationDurationInDays = spec2['activation_duration_in_days'],
            campaignEndsOn = spec2['campaign_ends_on'],
            category = spec2['category'],
            categoryTags = spec2['category_tags'],
            description = spec2['description'],
            excludedDates = spec2['excluded_dates'],
            expirationDate = spec2['expiration_date'],
            marketingFeeCurrencyCode = spec2['marketing_fee_currency_code'],
            marketingFeeRate = spec2['marketing_fee_rate'],
            marketingFeeValue = spec2['marketing_fee_value'],
            maxRedemptions = spec2['max_redemptions'],
            maximumCumulativeReward = spec2['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec2['maximum_reward_per_transaction'],
            merchantCategories = spec2['merchant_categories'],
            merchantExternalID = spec2['merchant_external_id'],
            merchantWebsite = spec2['merchant_website'],
            mode = spec2['mode'],
            rewardRate = spec2['reward_rate'],
            rewardValue = spec2['reward_value'],
            terms = spec2['terms'],
            validDayParts = spec2['valid_day_parts'],
        )

    assert offer.isCongruent()
    assert isinstance(offer, Offer)

    #omit field
    with pytest.raises(TypeError):
        Offer.create(
            currencyCode = spec2['currency_code'],
            effectiveDate = spec2['effective_date'],
            externalID = spec2['external_id'],
            headline = spec2['headline'],
            marketingFeeType = spec2['marketing_fee_type'],
            minimumSpend = spec2['minimum_spend'],
            rewardType = spec2['reward_type'],
            offerType = spec2['offer_type'],
            activationDurationInDays = spec2['activation_duration_in_days'],
            campaignEndsOn = spec2['campaign_ends_on'],
            category = spec2['category'],
            categoryTags = spec2['category_tags'],
            description = spec2['description'],
            excludedDates = spec2['excluded_dates'],
            expirationDate = spec2['expiration_date'],
            marketingFeeCurrencyCode = spec2['marketing_fee_currency_code'],
            marketingFeeRate = spec2['marketing_fee_rate'],
            marketingFeeValue = spec2['marketing_fee_value'],
            maxRedemptions = spec2['max_redemptions'],
            maximumCumulativeReward = spec2['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec2['maximum_reward_per_transaction'],
            merchantCategories = spec2['merchant_categories'],
            merchantExternalID = spec2['merchant_external_id'],
            merchantWebsite = spec2['merchant_website'],
            mode = spec2['mode'],
            rewardRate = spec2['reward_rate'],
            rewardValue = spec2['reward_value'],
            terms = spec2['terms'],
            validDayParts = spec2['valid_day_parts'],
        )

    # use input with bad format
    with pytest.raises(CallError):
        Offer.create(
            activationRequired = spec2['activation_required'],
            currencyCode = spec2['currency_code'],
            effectiveDate = spec2['effective_date'],
            externalID = spec2['external_id'],
            headline = spec2['headline'],
            marketingFeeType = spec2['marketing_fee_type'],
            minimumSpend = spec2['minimum_spend'],
            rewardType = spec2['reward_type'],
            offerType = spec2['offer_type'],
            activationDurationInDays = spec2['activation_duration_in_days'],
            campaignEndsOn = spec2['campaign_ends_on'],
            category = spec2['category'],
            categoryTags = spec2['category_tags'],
            description = spec2['description'],
            excludedDates = spec2['excluded_dates'],
            expirationDate = 'abc',
            marketingFeeCurrencyCode = spec2['marketing_fee_currency_code'],
            marketingFeeRate = spec2['marketing_fee_rate'],
            marketingFeeValue = spec2['marketing_fee_value'],
            maxRedemptions = spec2['max_redemptions'],
            maximumCumulativeReward = spec2['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec2['maximum_reward_per_transaction'],
            merchantCategories = spec2['merchant_categories'],
            merchantExternalID = spec2['merchant_external_id'],
            merchantWebsite = spec2['merchant_website'],
            mode = spec2['mode'],
            rewardRate = spec2['reward_rate'],
            rewardValue = spec2['reward_value'],
            terms = spec2['terms'],
            validDayParts = spec2['valid_day_parts'],
        )

    # use input with bad format - violates format not like a tax ID
    with pytest.raises(CallError):
        Offer.create(
            activationRequired = spec2['activation_required'],
            currencyCode = spec2['currency_code'],
            effectiveDate = spec2['effective_date'],
            externalID = '111-11-1111',
            headline = spec2['headline'],
            marketingFeeType = spec2['marketing_fee_type'],
            minimumSpend = spec2['minimum_spend'],
            rewardType = spec2['reward_type'],
            offerType = spec2['offer_type'],
            activationDurationInDays = spec2['activation_duration_in_days'],
            campaignEndsOn = spec2['campaign_ends_on'],
            category = spec2['category'],
            categoryTags = spec2['category_tags'],
            description = spec2['description'],
            excludedDates = spec2['excluded_dates'],
            expirationDate = spec2['expiration_date'],
            marketingFeeCurrencyCode = spec2['marketing_fee_currency_code'],
            marketingFeeRate = spec2['marketing_fee_rate'],
            marketingFeeValue = spec2['marketing_fee_value'],
            maxRedemptions = spec2['max_redemptions'],
            maximumCumulativeReward = spec2['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec2['maximum_reward_per_transaction'],
            merchantCategories = spec2['merchant_categories'],
            merchantExternalID = spec2['merchant_external_id'],
            merchantWebsite = spec2['merchant_website'],
            mode = spec2['mode'],
            rewardRate = spec2['reward_rate'],
            rewardValue = spec2['reward_value'],
            terms = spec2['terms'],
            validDayParts = spec2['valid_day_parts'],
        )

    with pytest.raises(CallError):
        Offer.create(
            activationRequired = spec2['activation_required'],
            currencyCode = spec2['currency_code'],
            effectiveDate = spec2['effective_date'],
            externalID = '111-11-1111',
            headline = spec2['headline'],
            marketingFeeType = spec2['marketing_fee_type'],
            minimumSpend = spec2['minimum_spend'],
            rewardType = spec2['reward_type'],
            offerType = spec2['offer_type'],
            activationDurationInDays = spec2['activation_duration_in_days'],
            campaignEndsOn = spec2['campaign_ends_on'],
            category = spec2['category'],
            categoryTags = spec2['category_tags'],
            description = spec2['description'],
            excludedDates = spec2['excluded_dates'],
            expirationDate = spec2['expiration_date'],
            marketingFeeCurrencyCode = spec2['marketing_fee_currency_code'],
            marketingFeeRate = spec2['marketing_fee_rate'],
            marketingFeeValue = spec2['marketing_fee_value'],
            maxRedemptions = spec2['max_redemptions'],
            maximumCumulativeReward = spec2['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec2['maximum_reward_per_transaction'],
            merchantCategories = spec2['merchant_categories'],
            merchantExternalID = spec2['merchant_external_id'],
            merchantWebsite = spec2['merchant_website'],
            mode = spec2['mode'],
            rewardRate = spec2['reward_rate'],
            rewardValue = spec2['reward_value'],
            terms = spec2['terms'],
            validDayParts = spec2['valid_day_parts'],
        )


def test_Offer_list():
    offers = Offer.list()
    assert isinstance(offers, list)
    lenFullList = len(offers)
    if len(offers):
        offer = offers[0]
        assert isinstance(offer, TripleObject)
        assert offer.isCongruent()

    # Specify pageSize
    offers = Offer.list(pageSize=4)
    assert isinstance(offers, list)
    if lenFullList < 4:
        assert len(offers) == lenFullList
    assert len(offers) == 4
    offer = offers[0]
    assert isinstance(offer, TripleObject)
    assert offer.isCongruent()

    # Specify merchant
    offers = Offer.list(merchantExternalID = _merchant.externalID)
    assert isinstance(offers, list)
    assert len(offers)>0
    for offer in offers:
        assert isinstance(offer,TripleObject)
        assert offer.isCongruent()
        assert offer.merchantExternalID == _merchant.externalID

    # Specify offer
    oneOffer = Offer.list(externalID = _offer.externalID)
    assert isinstance(oneOffer, list)
    assert len(oneOffer)==1
    assert isinstance(oneOffer[0], TripleObject)
    assert oneOffer[0].objID == _offer.objID


def test_Offer_byID():
    result = Offer.byID(_offer.objID)
    assert isinstance(result, Offer)

    assert not Offer.byID(None)
    assert not Offer.byID('bogus')


def test_Offer_updateWith():
    offer = Offer.byID(_offer.objID)
    effDate = offer.effectiveDate
    payload = { 'effective_date' : '2022-11-01', }
    result = Offer.updateWith(_offer.objID, payload)
    assert result.effectiveDate == '2022-11-01'
    # Reset:
    payload['effective_date'] = effDate
    result = Offer.updateWith(_offer.objID, payload)
    assert result.effectiveDate != '2022-11-01'

    # Provide message when object to change does not exist
    payload = { 'effective_date' : '2023-01-10', }
    with pytest.raises(InvalidPayloadError):
        result = Offer.updateWith('this_id_does_not_exist', payload)


def test_Offer_delete():
    offerID = _offer.externalID
    msg = Offer.delete(_offer.objID)
    assert msg == 'The resource was deleted successfully.'

    # recreate with previous objID

    spec = {
        'activation_required': False,
        'currency_code': 'USD',
        'effective_date': '2022-12-01',
        'external_id': 'offer-%s' % uuid.uuid4().hex,
        'headline': 'Get 5 Percent back on this Test Offer',
        'marketing_fee_type': 'PERCENTAGE',
        'minimum_spend': 0,
        'reward_type': 'PERCENTAGE',
        'offer_type': 'CARD_LINKED',
        'activation_duration_in_days': None,
        'campaign_ends_on': None,
        'category': 'FOOD',
        'category_tags': 'Catering, Delivery Services, Grocery Stores, Restaurants',
        'description': 'Test Offer Description',
        'excluded_dates': None,
        'expiration_date': None,
        'marketing_fee_currency_code': None,
        'marketing_fee_rate': 1.0,
        'marketing_fee_value': None,
        'max_redemptions': None,
        'maximum_cumulative_reward': None,
        'maximum_reward_per_transaction': None,
        'merchant_categories': None,
        'merchant_external_id': _merchant.externalID,
        'merchant_website': None,
        'mode': 'IN_PERSON',
        'reward_rate': 0.0,
        'reward_value': None,
        'terms': None,
        'valid_day_parts': None,
    }

    offer = Offer.create(
            activationRequired = spec['activation_required'],
            currencyCode = spec['currency_code'],
            effectiveDate = spec['effective_date'],
            externalID = offerID,
            headline = spec['headline'],
            marketingFeeType = spec['marketing_fee_type'],
            minimumSpend = spec['minimum_spend'],
            rewardType = spec['reward_type'],
            offerType = spec['offer_type'],
            activationDurationInDays = spec['activation_duration_in_days'],
            campaignEndsOn = spec['campaign_ends_on'],
            category = spec['category'],
            categoryTags = spec['category_tags'],
            description = spec['description'],
            excludedDates = spec['excluded_dates'],
            expirationDate = spec['expiration_date'],
            marketingFeeCurrencyCode = spec['marketing_fee_currency_code'],
            marketingFeeRate = spec['marketing_fee_rate'],
            marketingFeeValue = spec['marketing_fee_value'],
            maxRedemptions = spec['max_redemptions'],
            maximumCumulativeReward = spec['maximum_cumulative_reward'],
            maximumRewardPerTransaction = spec['maximum_reward_per_transaction'],
            merchantCategories = spec['merchant_categories'],
            merchantExternalID = spec['merchant_external_id'],
            merchantWebsite = spec['merchant_website'],
            mode = spec['mode'],
            rewardRate = spec['reward_rate'],
            rewardValue = spec['reward_value'],
            terms = spec['terms'],
            validDayParts = spec['valid_day_parts'],
        )

    assert isinstance(offer,TripleObject)
