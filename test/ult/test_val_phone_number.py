from validate.val_phone_number import val_phone_number as target
import pytest

def test_validator_return_type():
    assert isinstance(target("111-222-3333"), bool), "Unexpected failure: Function return type not bool"

def test_validator_correct_input():
    assert target("111-222-3333") == True, "Unexpected failure: Function rejected valid input format \"[3 nums]-[3 nums]-[4 nums]\""

def test_validator_invalid_type():
    assert target(1112223333) == False, "Expected failure: integer value passed as argument"

def test_validator_invalid_format_no_dashes():
    assert target("1112223333") == False, "Expected failure: Incorrect String Format passed: 10-ints/no-dashes"

def test_validator_invalid_format_incorrect_styling():
    assert target("(111)222-3333") == False, "Expected failure: Incorrect String Format passed: (area)num-num format"

def test_validator_invalid_char():
    assert target("aa1_bb2_cc33") == False, "Expected failure: Incorrect String passed: non-num + non-dash values"

def test_validator_input_too_long_area_code():
    assert target("1111-222-3333") == False, "Expected failure: Incorrect String passed: too-long -> area code"

def test_validator_input_too_long_body():
    assert target("111-2222-3333") == False, "Expected failure: Incorrect String passed: too-long -> body (middle segment)"

def test_validator_input_too_long_tail():
    assert target("111-222-33333") == False, "Expected failure: Incorrect String passed: too-long -> tail (end segment)"

def test_validator_input_too_short_area_code():
    assert target("11-222-3333") == False, "Expected failure: Incorrect String passed: too-short -> area code"

def test_validator_input_too_short_body():
    assert target("111-22-3333") == False, "Expected failure: Incorrect String passed: too-short -> body (middle segment)"

def test_validator_input_too_short_tail():
    assert target("111-222-3") == False, "Expected failure: Incorrect String passed: too-short -> tail (end segment)"