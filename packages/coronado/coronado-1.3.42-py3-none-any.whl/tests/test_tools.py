# vim: set fileencoding=utf-8:


from copy import deepcopy

from coronado.baseobjects import BASE_CARD_ACCOUNT_DICT
from coronado.tools import camelCaseOf
from coronado.tools import die
from coronado.tools import tripleKeysToCamelCase


# *** tests ***

def test_camelCaseOf():
    control = 'someText'

    assert camelCaseOf('Some Text') == control
    assert camelCaseOf('Some_Text') == control
    assert camelCaseOf('some.tExt') == control
    assert camelCaseOf('SomE/text') == control

    control = 'something'
    assert camelCaseOf('something') == control
    assert camelCaseOf('Something') == control

    control = 'somethingWTF' # test for acronym in field name
    assert camelCaseOf('something WTF') == control

    assert camelCaseOf('BBQ') == 'aBBQ'
    assert camelCaseOf('UFO') == 'aUFO'
    assert camelCaseOf('ELO') == 'anELO'

    assert camelCaseOf('ELO concert') == 'anELOConcert'
    assert camelCaseOf('CIA label') == 'aCIALabel'


def test_tripleKeysToCamelCase():
    d = deepcopy(BASE_CARD_ACCOUNT_DICT)
    d['card_bins'] = ['4444', '5555', ]
    d['mid'] = 6942
    d['processor_mid'] = 4269
    d['user_identity'] = 'secret'

    x = tripleKeysToCamelCase(d)

    assert 'objID' in x
    assert 'updatedAt' in x
    assert 'cardProgramID' in x
    assert 'userIdentity' in x
    assert 'processorMID' in x
    assert 'cardBINs' in x


def test_die():
    assert die("Message", 69, unitTest = True) == 69

