from firewall import Firewall
from logging_basic_config import logging_basic_config

logger = logging_basic_config()

class FortiGate(Firewall):
    def create_session(self):
        super().create_session()
        self.session.headers.update({"Authorization":f"Bearer {self.key}", "Content-Type":"application/json"})

    def get_addresses(self):
        url = f"https://{self.ip}/api/v2/cmdb/firewall/address"
        method="GET"
        params=None
        payload=None
        json_response=self.send_request(method=method,url=url,param=params,payload=None)
        logger.info(json_response)

    def create_addresses(self):
        pass

    def delete_addresses(self):
        pass