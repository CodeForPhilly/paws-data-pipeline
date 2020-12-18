import pytest
from user_api import check_password, hash_password


def test_pw_hashing():
    test_pw = "long complicated password ##$& λογοσ δοζα"
    assert check_password(test_pw, hash_password(test_pw))

