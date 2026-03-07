import utils.logger.logger as log
from services.connect_database import db_connection
import pandas as pd

def get_average_price(product_id):
    """
    :Gets the average item price from a list containing all price data for a product
    :args- price_data = list of dicts that contain the previous sales info 
    :returns aggregate mean as float on success, -1 on fail
    """
    price_data = _fetch_price_history(product_id)

    if price_data is None:
        log.error("price_data cannot be NoneType")
        return 0
    elif not price_data:
        log.error("price_data is empty")
        return 0
    
    dataframe = pd.DataFrame(price_data)
    
    if 'price' not in dataframe.columns:
        log.error("no price field found in price_data")
        return 0
    
    #Strip dollar signs
    dataframe['price'] = dataframe['price'].astype(str).str.replace('$', '')
    #Convert column to floats
    dataframe['price'] = pd.to_numeric(dataframe['price'], errors = 'coerce')
    
    average = dataframe['price'].mean()

    return average

def _fetch_price_history(product_id):
    try:
        container = db_connection.connect("Consignments")

        query = """
                    SELECT c.ticket_number, c.datetime, p.product_id, p.price
                    FROM c
                    JOIN p IN c.products
                    WHERE c.type = 'consignment'
                    AND p.product_id = @prod_id
                    """

        parameters = [{"name": "@prod_id", "value": product_id}]

        results = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        price_history = []
        for item in results:
            price_history.append({
                'product_id': item['product_id'],
                'ticket_number': item['ticket_number'],
                'datetime': item['datetime'],
                'price': item['price']
            })

        return price_history

    except Exception as e:
        log.error(f"Error fetching price_history: {e}")
        return []