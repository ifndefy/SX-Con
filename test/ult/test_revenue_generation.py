from ui.core.revenue_generation import RevenueGeneration as test_target
import pytest

def test_revenue_generation():
    #Test Rates values
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 100) == {"gross": 2.50, "vendor": 0.00, "super_x": 2.50}
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 50) == {"gross": 2.50, "vendor": 1.25, "super_x": 1.25}
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 100, rate = 100) == {"gross": 10.00, "vendor": 0.00, "super_x": 10.00}
    
def test_zero_rate():
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 100, rate = 0) == {"gross": 10.00, "vendor": 10.00, "super_x": 0.00}
    
def test_invalid_rates():
    #Invalid Rates test
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = -1) == -1 , "calculate_revenues did not return -1 on negative rate"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = 9999) == -1 , "calculate_revenues did not return -1 on rate over 100%"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = "ISHOULDN'TBETHIS") == -1, "calculate_revenues did not return -1 on NaN rate"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 25, rate = "WHATABOUTWITHA100%") == -1, "calculate_revenues did not return -1 on NaN rate with parsable chars"

def test_zero_percentile():
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 0, rate = 100), {"gross": 0.00, "vendor": 0.00, "super_x": 0.00}
    
def test_invalid_percentiles():
    #Invalid Percentile test
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = -1, rate = 20) == -1, "calculate_revenues did not return -1 on negative percentile"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on percentile over 100%"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = "ISHOULDN'TBETHIS", rate = 20) == -1,  "calculate_revenues did not return -1 on NaN percentile"
    assert test_target.calculate_revenues(price = 1.00, quantity = 10, percentile = "WHATABOUTWITHA100%", rate = 20) == -1, "calculate_revenues did not return -1 on NaN percentile with parsable chars"

def test_invalid_price():
    #Invalid price
    assert test_target.calculate_revenues(price = -1.00, quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on negative price"
    assert test_target.calculate_revenues(price = "hello", quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on NaN price"
    assert test_target.calculate_revenues(price = "$25hello", quantity = 10, percentile = 100, rate = 100) == -1, "calculate_revenues did not return -1 on NaN price with parsable chars"

def test_invalid_qty():
    #Invalid price
    assert test_target.calculate_revenues(price = 1.00, quantity = -1, percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity"
    assert test_target.calculate_revenues(price = 1.00, quantity = "hello", percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity"
    assert test_target.calculate_revenues(price = 1.00, quantity = "hello1", percentile = 9999, rate = 20) == -1, "calculate_revenues did not return -1 on NaN quantity with parsable chars"