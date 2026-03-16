import re

def val_entity_type(etype: str) -> bool:
    if not isinstance(etype, str): 
        return False
    
    regex = "^(consignment|user|vendor|product)$"
    return bool(re.search(regex, etype))