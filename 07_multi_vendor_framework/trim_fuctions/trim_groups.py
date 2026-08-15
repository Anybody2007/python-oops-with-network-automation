import logging
from logging_basic_config import logging_basic_config
logger = logging.getLogger(__name__)
def get_address_groups(json_response: dict) -> list:
    addr_groups = []
    for item in json_response:
        item_member = []
        item_name = item.get("name")
        for member in item.get("member", []):
            item_member.append(member.get("name"))
        addr_groups.append({"name":item_name, "member": item_member})
    logger.debug(addr_groups)
    return addr_groups