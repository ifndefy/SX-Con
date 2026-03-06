from services.get_item import get_item
from services.update_property import update_property
import utils.logger.logger as log

def _fetch_consignment(consignment_id: str):
    """
    :Purpose: gets the consignment doc from db
    :Param: consignment_id as a string
    :Author(s): Joe Lee
    """
    consignment = get_item("Consignments", "consignment", consignment_id)
    if consignment is None:
        log.error(f"Consignment not found: {consignment_id}")
        return None
    return consignment

def _find_product_index(products: list, product_id: str):
    """
    :Purpose: finds the index of the product in the displayed GUI
    :Param: products section list
    :Param: product_id as a string
    :Return: product index as an int
    :Author(s): Joe Lee
    """
    for i, prod in enumerate(products):
        if prod.get('product_id') == product_id:
            return i
    log.error(f"Product {product_id} not found in consignment")
    return None

def _validate_sold(new_sold: int, quantity: int):
    """
    :Purpose: validates the sold quantity
    :Param: new_sold int
    :Param: quantity int
    :Author(s): Joe Lee
    """
    if new_sold < 0:
        log.error("Sold cannot be negative")
        return False
    if new_sold > quantity:
        log.error(f"Cannot sell more than signed quantity ({quantity})")
        return False
    return True

def _update_sold(consignment_id: str, idx: int, new_sold: int):
    """
    :Purpose: updates the sold field for the given product index
    :Param: consignment_id as a string
    :Param: index as an integer
    :Param: new_sold as an integer
    :Author(s): Joe Lee
    """
    sold_path = f"products[{idx}].sold"
    result = update_property("Consignments", "consignment", consignment_id, sold_path, new_sold)
    if result != 0:
        log.error(f"Remaining update failed after sold update for product {idx}")
        return False
    return True

def _update_remaining(consignment_id: str, idx: int, new_remaining: int):
    """
    :Purpose: updates the remaining field for the given product index
    :Param: consignment_id as a string
    :Param: index as an integer
    :Param: new_remaining as an integer
    :Author(s): Joe Lee
    """
    remaining_path = f"products[{idx}].remaining"
    result = update_property("Consignments", "consignment", consignment_id, remaining_path, new_remaining)
    if result != 0:
        log.error(f"Remaining update failed after sold update for product at index {idx}")
        return False
    return True

def update_quantities(consignment_id: str, product_id: str, new_sold: int):
    """
    :Purpose: Update a product's sold and remaining fields in a consignment
    :Return: bool, new_remaining, and empty string
    :Author(s): Joe Lee
    """
    consignment = _fetch_consignment(consignment_id)
    products = consignment.get('products', [])
    idx = _find_product_index(products, product_id)
    quantity = products[idx].get('quantity', 0)
    if not _validate_sold(new_sold, quantity):
        log.error(f"Sold value exceeds signed value ({idx})")
        return False
    if not _update_sold(consignment_id, idx, new_sold):
        log.error(f"Failed to update sold ({idx})")
        return False
    new_remaining = quantity - new_sold
    if not _update_remaining(consignment_id, idx, new_remaining):
        return False
    return True, new_remaining, ""