from firewall import Firewall
from logging_basic_config import logging_basic_config
import logging

logging_basic_config()
logger = logging.getLogger(__name__)

class PaloAlto(Firewall):
    def __init__(self, hostname: str, vendor: str, username: str, ip: str, key: str, panorama_managed: bool = False):
        super().__init__(hostname, vendor, username, ip, key)
        self.header = {"X-PAN-KEY" : self.key}
        self.panorama_managed = panorama_managed

    def get_addresses(self):
        url = f"https://{self.ip}/restapi/v10.0/Objects/Addresses"
        params = {"location":"vsys","vsys":"vsys1"}
        json_response = self.send_request(methods="get",payloads=None,urls=url,param=params)
        entry_list = json_response.get("result",{}).get("entry",[])
        logger.info(f" HTTP : {json_response}")

    def create_addresses(self):
        url = f"https://{self.ip}/restapi/v10.0/Objects/Addresses"
        payload = {"entry":[{"@name":"Try","@location":"vsys","@vsys":"vsys1","ip-netmask":"1.1.1.1"}]}
        param = {}
        json_response = self.send_request(methods="post",payloads=payload,urls=url,param=param)