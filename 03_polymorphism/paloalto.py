from firewall import Firewall
from logging_basic_config import logging_basic_config

logger = logging_basic_config()

class PaloAlto(Firewall):
    def create_session(self):
        super().create_session()
        self.session.headers.update({"X-PAN-KEY": self.key})

    def get_addresses(self):
        url = f"https://{self.ip}/restapi/v10.0/Objects/Addresses"
        method = "GET"
        param = {"location":"vsys","vsys":"vsys1"}
        json_response = self.send_request(method=method,url=url,param=param)
        logger.info(json_response)