import logging
import ipaddress

from logging_basic_config import logging_basic_config
logger = logging.getLogger(__name__)
def get_exsiting_address(json_response: dict) -> tuple[list, list]:
    exsiting_ips = []
    exsiting_fqdns = []
    for item in json_response:
        item_type = item.get("type")
        item_name = item.get("name")
        if item_type == "ipmask":
            item_ip, item_network = item.get("subnet").split()
            item_subnet = str(ipaddress.IPv4Network(f"{item_ip}/{item_network}"))
            exsiting_ips.append({"name":item_name, "ip": item_subnet})
        elif item_type == "fqdn":
            item_fqdn = item.get("fqdn")
            exsiting_fqdns.append({"name":item_name, "fqdn": item_fqdn})
    logger.debug(exsiting_fqdns)
    logger.debug(exsiting_ips)
    return exsiting_fqdns, exsiting_ips