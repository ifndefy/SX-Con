from validate.val_entity_type import val_entity_type as target
import pytest

def test_validator_return_type():
    assert isinstance(target("user"), bool), "Unexpected failure: Function return type not bool"

def test_validator_correct_input():
    assert target("consignment") == True, "Unexpected failure: Function rejected valid input type: consignment"
    assert target("user") == True, "Unexpected failure: Function rejected valid input type: user"
    assert target("vendor") == True, "Unexpected failure: Function rejected valid input type: vendor"
    assert target("product") == True, "Unexpected failure: Function rejected valid input type: product"

def test_validator_invalid_type():
    assert target(1112223333) == False, "Expected failure: non-string value passed as argument"

def test_validator_invalid_input():
    assert target("users") == False, "Expected failure: Incorrect String Format passed: mis-spelled etype"

def test_validator_invalid_capitalization():
    assert target("uSEr") == False, "Expected failure: Incorrect String Format passed: mixed-caps"

def test_validator_multiple_packed():
    assert target("userconsignment") == False, "Expected failure: Incorrect String Format passed: multiple etypes passed at once"

def test_validator_multiple_spaced():
    assert target("user consignment") == False, "Expected failure: Incorrect String Format passed: multiple etypes passed with delimiter"

def test_validator_etype_dne():
    assert target("thisshouldbefalse") == False, "Expected failure: Incorrect String passed: etype does not exist"