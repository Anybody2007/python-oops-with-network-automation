import logging
import csv
from pathlib import Path
import sys
import ipaddress

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Firewall:
    def __init__(self,hostname, vendor, mgmt_ip, username, password):
        self.hostname = hostname
        self.vendor = vendor
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password

    def show_info(self):
        logger.info("="*20)
        logger.info(f"Hostname : {self.hostname}")
        logger.info(f"Vendor   : {self.vendor}")
        logger.info(f"IP       : {self.mgmt_ip}")
        logger.info(f"Username : {self.username}")
        logger.info(f"Password : **************")
        logger.info("="*20)

def inventory_loader(csv_file, vendor_list):
    if not Path(csv_file).exists():
        logger.error("Please check your file, it is not present")
        sys.exit(1)
    firewall_entry = []
    with open(file=csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for line, device in enumerate(reader, start=2):
            hostname = device.get("hostname", "")
            vendor = device.get("vendor", "")
            mgmt_ip = device.get("management_ip", "")
            username = device.get("username", "")
            password = device.get("password", "")
            response_content_verify = content_verify(line, hostname, vendor, mgmt_ip, username, password, vendor_list)
            if not response_content_verify.get("error"):
                logger.warning(response_content_verify.get("message"))
                continue
            logger.debug(response_content_verify.get("message"))
            current_firewall = Firewall(hostname,vendor,mgmt_ip,username,password)
            firewall_entry.append(current_firewall)
        return firewall_entry


def content_verify(line, hostname, vendor, mgmt_ip, username, password, vendor_list):
    if not hostname:
        logger.warning(f"Line: {line}, hostname is blank. Skipping")
        return {"error" : True, "message" : f"Line {line} Hostname invalid"}
    if vendor not in vendor_list:
        logger.warning(f"Line: {line}, vendor is unknown. Skipping")
        return {"error" : True, "message" : f"Line {line} vendor {vendor} invalid"}
    try:
        ipaddress.ip_network(mgmt_ip, strict=False)
    except ValueError:
        logger.warning(f"Line: {line}, ip is invalid '{mgmt_ip}'. Skipping")
        return {"error" : True, "message" : f"Line {line} management ip {mgmt_ip} is invalid"}
    if not username:
        logger.warning(f"Line: {line}, username is blank. Skipping")
        return {"error" : True, "message" : f"Line {line} username blank"}
    if not password:
        logger.warning(f"Line: {line}, password is blank. Skipping")
        return {"error" : True, "message" : f"Line {line} password invalid"}
    return {"error" : False, "message" : f"All checks are passed for line no {line}"}

def main():
    csv_inventory = "inventory.csv"
    firewall_inventory_list = inventory_loader(csv_inventory, ["Fogtigate","Palo Alto"])
    print(firewall_inventory_list)
    for firewall in firewall_inventory_list:
        firewall.show_info()

if __name__ == "__main__":
    main()