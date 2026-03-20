from ui.core.revenue_generation import RevenueGeneration as target
import pytest

def test_revenue_generation():
    #Test Rates values
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 100) == {"gross": 2.50, "vendor": 0.00, "super_x": 2.50}, "Expected super_x to receive all revenue with rate 100"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 50) == {"gross": 2.50, "vendor": 1.25, "super_x": 1.25}, "Expected equal revenues for rate 50"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 100, rate = 100) == {"gross": 10.00, "vendor": 0.00, "super_x": 10.00}, "Expected super_x to receive all revenue with rate 100"
    
def test_zero_rate():
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 100, rate = 0) == {"gross": 10.00, "vendor": 10.00, "super_x": 0.00}, "Expected vendor to receive all revenue with rate 0"
    
def test_invalid_rates():
    #Invalid Rates test
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = -1) == -1 , "calculate_revenues did not return -1 on negative rate"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 9999) == -1 , "calculate_revenues did not return -1 on rate over 100%"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = "ISHOULDN'TBETHIS") == -1, "calculate_revenues did not return -1 on NaN rate"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = "WHATABOUTWITHA100%") == -1, "calculate_revenues did not return -1 on NaN rate with parsable chars"

def test_zero_percentile():
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 0, rate = 100) == {"gross": 0.00, "vendor": 0.00, "super_x": 0.00}, "Expected generation to fail and show 0.00 for all sides"
    
def test_invalid_percentiles():
    #Invalid Percentile test
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = -1, rate = 20) == -1, "calculate_revenues did not return -1 on negative percentile"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on percentile over 100%"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = "ISHOULDN'TBETHIS", rate = 20) == -1,  "calculate_revenues did not return -1 on NaN percentile"
    assert target.calculate_revenues(price = 1.00, quantity = 10, percentile = "WHATABOUTWITHA100%", rate = 20) == -1, "calculate_revenues did not return -1 on NaN percentile with parsable chars"

def test_invalid_price():
    #Invalid price
    assert target.calculate_revenues(price = -1.00, quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on negative price"
    assert target.calculate_revenues(price = "hello", quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on NaN price"
    assert target.calculate_revenues(price = "$25hello", quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on NaN price with parsable chars"

def test_invalid_qty():
    #Invalid price
    assert target.calculate_revenues(price = 1.00, quantity = -1, percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity"
    assert target.calculate_revenues(price = 1.00, quantity = "hello", percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity"
    assert target.calculate_revenues(price = 1.00, quantity = "hello1", percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity with parsable chars"