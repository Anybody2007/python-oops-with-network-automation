from firewall import Firewall
from logging_basic_config import logging_basic_config

logger = logging_basic_config()

class Fortigate(Firewall):
    def create_session(self):
        super().create_session()
        self.session.headers.update({"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"})

    def get_addresses(self):
        url = f"https://{self.ip}/api/v2/cmdb/firewall/address"
        method = "GET"
        json_response = self.send_request(method=method,url=url)
        logger.info(json_response)