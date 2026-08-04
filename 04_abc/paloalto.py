from logging_basic_config import logging_basic_config
from firewall import Firewall

logger = logging_basic_config()

class PaloAlto(Firewall):
    def create_session(self):
        super().create_session()
        self.session.headers.update({"X-PAN-KEY":f"{self.key}", "Content-Type": "application/json"})

    def get_addresses(self):
        url = f"https://{self.ip}/restapi/v10.0/Objects/Addresses"
        param={"location":"vsys","vsys":"vsys1"}
        method="GET"
        payload=None
        json_response=self.send_request(method=method,url=url,param=param,payload=payload)
        logger.info(json_response)

    def create_addresses(self):
        pass

    def delete_addresses(self):
        pass