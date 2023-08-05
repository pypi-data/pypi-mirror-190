# vim: set fileencoding=utf-8:


from coronado.exceptions import ForbiddenError
from coronado.exceptions import UnexpectedError
from coronado.exceptions import errorFor

import json


# +++ tests +++

def test_errorFor():
    details = "No permissions, fam!"
    e = errorFor(403, details)

    eJSON = json.loads(str(e))

    assert isinstance(e, ForbiddenError)
    assert details == eJSON['tripleInfo']

    e = errorFor(-1)
    assert isinstance(e, UnexpectedError)

    e = errorFor(400, json.dumps({ 'xxxx': 'blah', 'exception': 'bleh', }))

    eJSON = json.loads(str(e))
    assert eJSON['errno'] == 400
    assert eJSON['tripleInfo']['serviceException'] == 'bleh'

