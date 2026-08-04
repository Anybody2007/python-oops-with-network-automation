from logging_basic_config import logging_basic_config
import logging
from paloalto import PaloAlto
from fortigate import Fortigate
import urllib3

urllib3.disable_warnings()

logging_basic_config()
logger = logging.getLogger(__name__)

def main():
    fortigate = Fortigate(hostname="FGT-HQ",vendor="FortiGate",username="admin",ip="192.168.35.249",key="h36bGs4p5rpcmNwf8dw7Hrs5Qq50hQ")
    paloalto = PaloAlto(hostname="PA-HQ",vendor="PaloAlto",username="admin",ip="192.168.35.248",key="LUFRPT0zVTZKMldwdE5qd21DeWVtaG5vZGFQT3pjS0U9bkJodVJ5VDVQanJDdVVYNFFPbm5MNFdoL0R6TkltU2cvVDNsa0FpWjZhb2xweUt1T1lPdmhUbkJPbTVyVGQ3dA==")
    firewalls = [fortigate,paloalto]
    for firewall in firewalls:
        firewall.show_info()
        firewall.create_session()
        firewall.get_addresses()

if __name__ == "__main__":
    main()