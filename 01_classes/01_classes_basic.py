import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Firewall:
    def show_info(self, hostname, vendor, mgmt_ip, username, password):
        logger.info("="*20)
        logger.info(f"Hostname : {hostname}")
        logger.info(f"Vendor   : {vendor}")
        logger.info(f"IP       : {mgmt_ip}")
        logger.info(f"Username : {username}")
        logger.info(f"Password : {password}")
        logger.info("="*20)

def main():
    hostname = "FGT-HQ"
    vendor = "Fortigate"
    mgmt_ip = "192.168.35.248"
    username = "admin"
    password = "abcd1234"
    firewall_1 = Firewall()
    firewall_1.show_info(hostname, vendor, mgmt_ip, username, password)

if __name__ == "__main__":
    main()