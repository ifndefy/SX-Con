import re
import utils.logger.logger as log


def val_entity_type(etype: str) -> bool:
    """
    :purpose: Validate that the entity type is one of the three acceptable types
    
    :return: True on success, False on Fail
    :authors: Maksym Komarov
    """
    if not isinstance(etype, str):
        log.error("Entity type must be string")
        return False
    
    regex = r"^(Consignment|User|Vendor|Product)$"

    if bool(re.search(regex, etype)):
        return True
    else:
        log.error("Invalid entity type")
        return False