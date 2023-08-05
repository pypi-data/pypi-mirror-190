from coronado.daterange import DateRange


# *** tests ***

def test_DateRange():
    reward = DateRange('YTD')
    assert reward == DateRange.YTD

