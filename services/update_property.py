from services.connect_database import db_connection
from src import SPOT

def update_property(container_name: str, entity_type: str, entity_id: str, property_name: str, property_value):
    if SPOT.OFFLINE:
        print("OFFLINE - Invalid Action - Requires network access")
        return 0

    try:
        container = db_connection.connect(container_name)
        item_id = f"{entity_type}_{entity_id}"

        existing_item = container.read_item(item=item_id, partition_key=item_id)

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
        print(f"Successfully updated {property_name} for {item_id}")
        return 0

    except Exception as e:
        print(f"Error in update_property: {e}")
        return None