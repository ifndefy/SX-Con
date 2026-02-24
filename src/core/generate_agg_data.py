"""
Defines methods to generate aggregate data
"""
import utils.logger.logger as log
from services.connect_database import db_connection


def agg_total_product_type(product_doc: list, product_type: str) -> float:
    """
    :Purpose: generates aggregate data for all products in an item grouped by product type
    :Parameter: product_doc: product document
    :Method: takes product doc list which nests dictionaries, then groups by product type, then finds aggregate totals
    :Author(s): Joe Lee
    """
    wanted_prod_type = product_type.strip().lower()
    total = 0.0
    for prod in product_doc:
        prod_type = prod.get("product_type", '').strip().lower()
        if prod_type != wanted_prod_type:
            continue
        price = prod.get('price', '0')
        qty = int(prod.get('quantity', '0'))
        if not val_price(price):
            fixed_price = convert_price(price)
        else:
            fixed_price = price
        total += fixed_price * qty
    return round(total, 2)

def avg_product_price(product_id: int|str) -> float:
    """
    :Purpose: generates aggregate data for a single product by product_id
    :Method: fetches the DB for the prices of product_id, then finds average
    :Return: average price
    :Author(s): Joe Lee
    """
    try:
        container = db_connection.connect('Consignments')
        prices_raw = fetch_product_prices(container, str(product_id))

        if not prices_raw:
            return 0.0

        total = 0.0
        count = 0
        for price_str in prices_raw:
            if val_price(price_str):
                price_val = float(price_str)
            else:
                price_val = convert_price(price_str)
                if price_val is None:
                    price_val = 0.0

            if price_val > 0:
                total += price_val
                count += 1

        if count > 0:
            avg = total / count
        else:
            avg = 0.0
        return round(avg, 2)

    except Exception as e:
        log.error(f"Error calculating average price for product {product_id}: {e}")
        return 0.0

def val_price(price) -> bool:
    """
    :Purpose: Verifies that price is a float
    """
    if isinstance(price, float):
        return True
    else:
        return False

def convert_price(price) -> float|None:
    """
    :Purpose: converts price to float
    """
    try:
        if isinstance(price, int):
            return float(price)
        if isinstance(price, str):
            if price.startswith("$"):
                return float(price[1:])
    except Exception as e:
        log.error("Failed to convert price to float: {}".format(e))
        return None

def fetch_product_prices(container, product_id):
    query = """
            SELECT p.price
            FROM c 
            JOIN p IN c.price_data.products
            WHERE c.type = 'consignment' AND p.product_id = @product_id
            """
    parameters = [{"name": "@product_id", "value": product_id}]
    items = container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    )
    prices = []
    for item in items:
        prices.append(item['price'])
    return prices