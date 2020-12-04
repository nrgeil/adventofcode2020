import pytest


@pytest.fixture(scope="function")
def test_passport():
    return {
        "eyr": "2030",
        "cid": "100",
        "hcl": "#623a2f",
        "ecl": "amb",
        "hgt": "74in",
        "pid": "087499704",
        "iyr": "2012",
        "byr": "1980",
    }
