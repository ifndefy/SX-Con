from services.connect_database import db_connection
from services.get_property import get_property
from src import SPOT
import utils.logger.logger as log

def update_property(container_name: str, entity_type: str, entity_id: str, property_name: str, property_value, silent: bool = False):
    """
    :param container_name: Container Name
    :param entity_type: Entity Type
    :param entity_id: Entity ID
    :param property_name: Property Name
    :param property_value: Property Value
    :author(s): Joe Lee, Maksym Komarov
    """
    if SPOT.OFFLINE:
        log.warning("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)
        item_id = f"{entity_type}_{entity_id}"

        existing_item = container.read_item(item=item_id, partition_key=item_id)

        if entity_type == "user":
            display_name = get_property(container_name, "username", entity_type, entity_id)
        elif entity_type == "vendor":
            v_id = get_property(container_name, "vendor_id", entity_type, entity_id)
            v_fname = get_property(container_name, "first_name", entity_type, entity_id)
            v_lname = get_property(container_name, "last_name", entity_type, entity_id)
            display_name = " ".join([v_id, v_fname, v_lname])
        elif entity_type == "product":
            p_id = get_property(container_name, "product_id", entity_type, entity_id)
            p_name = get_property(container_name, "product_name", entity_type, entity_id)
            display_name = " ".join([p_id, p_name])
        elif entity_type == "consignment":
            display_name = f"Ticket Number {entity_id}"
        else:
            raise Exception(f"Unknown entity type: {entity_type}")

        if not silent:
            log.info(f"Updating '{property_name}' for {display_name} -> {property_value!r}")

        if '.' in property_name or '[' in property_name:
            keys = property_name.replace('[', '.').replace(']', '').split('.')
            current = existing_item
            for key in keys[:-1]:
                if key.isdigit():
                    current = current[int(key)]
                else:
                    current = current[key]
            last_key = keys[-1]
            if last_key.isdigit():
                current[int(last_key)] = property_value
            else:
                current[last_key] = property_value
        else:
            existing_item[property_name] = property_value

        container.replace_item(item=item_id, body=existing_item)
        if not silent:
            log.info(f"Successfully updated {property_name} for {display_name}")
        return 0

    except Exception as e:
        log.error(f"Error in update_property: {e}")
        return None