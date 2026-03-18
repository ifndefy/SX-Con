import re

def val_entity_type(etype: str) -> bool:
    if not isinstance(etype, str): 
        return False
    
    regex = r"^(Consignment|User|Vendor|Product)$"
    return bool(re.search(regex, etype))