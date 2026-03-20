from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log


def get_latest_rate(product_id: int) -> int:
    """
    :purpose: gets the most recent rate applied to a product
    :param: product_id
    :author(s): Joe lee
    """

    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect("Consignments")

        query = """
            SELECT p.rate
            FROM c
            JOIN p IN c.products
            WHERE c.entity_type = 'consignment'
            AND p.product_id = @prod_id
            ORDER BY c.datetime DESC
            OFFSET 0 LIMIT 1
        """

        parameters = [{"name": "@prod_id", "value": product_id}]

        results = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

        if results and results[0].get('rate') is not None:
            return int(results[0]['rate'])

        log.info(f"Did not find a used rate for product_id: {product_id}")
        return 0

    except Exception as e:
        log.error(f"Error getting latest rate from DB: {e}")
        return 0