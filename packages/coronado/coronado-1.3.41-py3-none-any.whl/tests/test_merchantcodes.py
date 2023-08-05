from coronado.merchantcodes import MerchantCategoryCode


# --- constants ---

VALID_TEST_MCC = '1740'


# +++ tests +++

def test_MerchantCategoryCode():
    merchantCode = MerchantCategoryCode(VALID_TEST_MCC)
    assert isinstance(merchantCode, MerchantCategoryCode)
    assert 'Masonry' in merchantCode.description

    # Create object from existing MCC or TripleObject
    merchantCode = MerchantCategoryCode(merchantCode)
    assert isinstance(merchantCode, MerchantCategoryCode)
    assert 'Masonry' in merchantCode.description


def test_MerchantCategoryCode_list():
    merchantCodes = MerchantCategoryCode.list()
    assert merchantCodes
    assert len(merchantCodes) > 500 # full list

    merchantCodes = MerchantCategoryCode.list(begin = '1500', end = '3000')
    assert len(merchantCodes) > 10

