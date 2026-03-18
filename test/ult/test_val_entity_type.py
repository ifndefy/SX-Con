from validate.val_entity_type import val_entity_type as target
import pytest

def test_validator_return_type():
    assert isinstance(target("User"), bool), "Unexpected failure: Function return type not bool"

def test_validator_correct_input():
    assert target("Consignment") == True, "Unexpected failure: Function rejected valid input type: Consignment"
    assert target("User") == True, "Unexpected failure: Function rejected valid input type: User"
    assert target("Vendor") == True, "Unexpected failure: Function rejected valid input type: Vendor"
    assert target("Product") == True, "Unexpected failure: Function rejected valid input type: Product"

def test_validator_invalid_type():
    assert target(1112223333) == False, "Expected failure: non-string value passed as argument"

def test_validator_invalid_input():
    assert target("Users") == False, "Expected failure: Incorrect String Format passed: mis-spelled etype"

def test_validator_invalid_capitalization():
    assert target("uSEr") == False, "Expected failure: Incorrect String Format passed: mixed-caps"

def test_validator_multiple_packed():
    assert target("UserConsignment") == False, "Expected failure: Incorrect String Format passed: multiple etypes passed at once"

def test_validator_multiple_spaced():
    assert target("User Consignment") == False, "Expected failure: Incorrect String Format passed: multiple etypes passed with delimiter"

def test_validator_etype_dne():
    assert target("thisshouldbefalse") == False, "Expected failure: Incorrect String passed: etype does not exist"