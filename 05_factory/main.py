from paloalto import PaloAlto
from fortigate import FortiGate
from factory import Factory
from logging_basic_config import logging_basic_config
import urllib3
urllib3.disable_warnings()
logger = logging_basic_config()

def firewall_factory(vendor_class_map: dict, entry: list) -> list:
    firewall_list = []
    for item in entry:
        firewall = vendor_class_map.get(item.get("vendor"))
        fw = firewall(vendor=item.get("vendor"),ip=item.get("ip"),key=item.get("key"))
        firewall_list.append(fw)
    return firewall_list

def main():
    entry = [{"vendor": "FortiGate","ip": "192.168.35.249","key": "h36bGs4p5rpcmNwf8dw7Hrs5Qq50hQ"},
             {"vendor": "PaloAlto", "ip": "192.168.35.248","key":"LUFRPT0zVTZKMldwdE5qd21DeWVtaG5vZGFQT3pjS0U9bkJodVJ5VDVQanJDdVVYNFFPbm5MNFdoL0R6TkltU2cvVDNsa0FpWjZhb2xweUt1T1lPdmhUbkJPbTVyVGQ3dA=="}]
    firewall_list = []
    for item in entry:
        fw = Factory(ip=item.get("ip"),vendor=item.get("vendor"),key=item.get("key"))
        firewall = fw.create_firewall()
        firewall_list.append(firewall)
        
    for firewall in firewall_list:
        firewall.show_info()
        firewall.create_session()
        firewall.get_addresses()

if __name__ == "__main__":
    main()