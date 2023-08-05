from copy import deepcopy

from coronado.strictaddress import StrictAddress
from coronado.baseobjects import BASE_ADDRESS_DICT
from coronado.exceptions import InvalidPayloadError

from tests.test_address import _ADDRESS

import pytest


# +++ tests +++

def test_StrictAddress_validate():

    inputAddress = deepcopy(BASE_ADDRESS_DICT)
    assert StrictAddress(inputAddress).validate() is None

    inputAddress = _ADDRESS.asSnakeCaseDictionary()
    del inputAddress['complete']
    assert StrictAddress(inputAddress).validate() is None

    assert StrictAddress(_ADDRESS).validate() is None
    inputAddress = _ADDRESS
    inputAddress.postalCode = '15212'
    assert StrictAddress(inputAddress).validate() is None

    with pytest.raises(InvalidPayloadError):
        inputAddress = _ADDRESS
        inputAddress.postalCode = ''
        StrictAddress(inputAddress).validate()

    with pytest.raises(InvalidPayloadError):
        inputAddress.postalCode = '123456789123456789'
        StrictAddress(inputAddress).validate()

    with pytest.raises(InvalidPayloadError):
        inputAddress = _ADDRESS
        inputAddress.countryCode = ''
        StrictAddress(inputAddress).validate()

    with pytest.raises(InvalidPayloadError):
        inputAddress = _ADDRESS
        inputAddress.countryCode = '12'
        StrictAddress(inputAddress).validate()

    with pytest.raises(InvalidPayloadError):
        inputAddress.countryCode = 'USA'
        StrictAddress(inputAddress).validate()

    with pytest.raises(InvalidPayloadError):
        inputAddress = _ADDRESS
        inputAddress.streetAddress = ''
        StrictAddress(inputAddress).validate()

