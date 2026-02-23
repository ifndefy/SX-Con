"""
Defines methods to generate aggregate data
"""
import utils.logger.logger as log

def agg_product_type(product_id: int) -> float:
    """
    :Purpose: generates aggregate data for all products in an item grouped by product type
    """
    pass

def agg_product() -> float:
    """
    :Purpose: generates aggregate data for a single product by product_id
    """
    pass

def get_total(price, qty: int) -> float:
    """
    :Purpose: generates the total for a product
    :Method: qty * price
    """
    fixed_price = 0
    if not val_price(price):
        fixed_price = convert_price(price)
    total = fixed_price * qty
    return total

def val_price(price) -> bool:
    """
    :Purpose: Verifies that price is a float
    """
    if price.isfloat():
        return True
    else:
        return False

def convert_price(price) -> float|None:
    """
    :Purpose: converts price to float
    """
    try:
        if price.isinteger():
            return float(price)
        if price.isstring():
            if price.startswith("$"):
                return float(price[1:])
        if price.isdecimal():
            return float(price)
    except Exception as e:
        log.error("Failed to convert price to float: {}".format(e))
        return None