from firewall import Firewall, register_firewall
from logging_basic_config import logging_basic_config
import logging

logging_basic_config()
logger = logging.getLogger(__name__)

@register_firewall("FortiGate")
class Fortigate(Firewall):
    def get_header(self):
        self.header = {"Authorization" : f"Bearer {self.key}"}

    def get_addresses(self):
        url = f"https://{self.ip}/api/v2/cmdb/firewall/address"
        response = self.send_request(methods="get",urls=url, payloads=None, param=None)
        logger.info(f" HTTP : {response}")
        return response

    def create_addresses(self, payload : dict) -> dict:
        url = f"https://{self.ip}/api/v2/cmdb/firewall/address"
        header = self.buid_header()
        response = self.send_request(methods="post",urls=url, payloads=payload, param=None)
        logger.info(f" HTTP : {response}")
        return response
        