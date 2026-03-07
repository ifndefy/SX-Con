import utils.logger.logger as log
from ui.core.revenue_generation import RevenueGeneration


def agg_total_product_type(product_doc: list, product_type: str) -> float | None:
    """
    :Purpose: generates aggregate data for all products in an item grouped by product type
    :Parameter: product_doc, a dictionary holding details of product(s)
    :Parameter: product_type, a string holding product type
    :Author(s): Joe Lee
    """
    wanted_prod_type = product_type.strip().lower()
    total = 0.0
    for prod in product_doc:
        prod_type = prod.get("product_type", '').strip().lower()
        if prod_type != wanted_prod_type:
            continue
        price = convert_price(prod.get('price', 0))
        if price is None:
            continue
        qty = prod.get('quantity', 0)
        rate = prod.get('rate', 0)
        result = RevenueGeneration.calculate_revenues(price, qty, "100%", 100 - rate)
        if result == -1:
            continue
        total += float(result['vendor'])
        return round(total, 2)

def convert_price(price) -> float | None:
    """
    :Purpose: converts price to float
    :Author(s): Joe Lee
    """
    try:
        if isinstance(price, float):
            return price
        if isinstance(price, int):
            return float(price)
        if isinstance(price, str):
            cleaned = price.strip().replace('$', '').replace(',', '')
            return float(cleaned)
    except Exception as e:
        log.error("Failed to convert price to float: {}".format(e))
        return None