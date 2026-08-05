from paloalto import PaloAlto
from fortigate import FortiGate
from logging_basic_config import logging_basic_config
logger = logging_basic_config()

class Factory():
    def __init__(self, ip:str, key:str, vendor:str):
        self.ip = ip
        self.key = key
        self.vendor = vendor
        self.vendor_dict = {"FortiGate":FortiGate,"PaloAlto":PaloAlto}

    def create_firewall(self):
        fw = self.vendor_dict.get(self.vendor)
        firewall = fw(vendor=self.vendor,ip=self.ip,key=self.key)
        return firewall