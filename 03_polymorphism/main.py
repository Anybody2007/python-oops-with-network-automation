from logging_basic_config import logging_basic_config
from firewall import Firewall
from paloalto import PaloAlto
from fortigate import Fortigate
import urllib3

urllib3.disable_warnings()

logger = logging_basic_config()

def main():
    firewall_list = []
    fortigate = Fortigate(vendor="FortiGate",ip="192.168.35.249",key="h36bGs4p5rpcmNwf8dw7Hrs5Qq50hQ")
    paloalto = PaloAlto(vendor="PaloAlto", ip="192.168.35.248",key="LUFRPT0zVTZKMldwdE5qd21DeWVtaG5vZGFQT3pjS0U9bkJodVJ5VDVQanJDdVVYNFFPbm5MNFdoL0R6TkltU2cvVDNsa0FpWjZhb2xweUt1T1lPdmhUbkJPbTVyVGQ3dA==")
    firewall_list = [fortigate,paloalto]
    for firewall in firewall_list:
        firewall.show_info()
        firewall.create_session()
        firewall.get_addresses()
if __name__ == "__main__":
    main()