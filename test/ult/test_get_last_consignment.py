from src.core.get_last_consignment import get_last_consignment

def test_get_last_consignment():
    assert get_last_consignment("user", "8") is not None, "Expected a last consignment value for user 8"
    assert get_last_consignment("vendor", "1") is not None, "Expected a last consignment value for vendor 1"
    assert get_last_consignment("product", "123519") is None, "Expected a fail for product 123519"