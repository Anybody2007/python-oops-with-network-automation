from abc import abstractmethod, ABC
from logging_basic_config import logging_basic_config
import requests

logger = logging_basic_config()

class Firewall(ABC):
    def __init__(self, ip: str, key: str, vendor: str):
        self.ip=ip
        self.key=key
        self.vendor=vendor
        self.loggedin=False

    def show_info(self):
        logger.info("="*20)
        logger.info(f"IP : {self.ip}")
        logger.info(f"Key : {self.key}")
        logger.info(f"Vendor : {self.vendor}")

    @abstractmethod
    def create_session(self):
        self.session = requests.Session()
        self.session.verify=False
        self.loggedin=True

    def send_request(self,method:str,url:str,param:dict,payload:dict) -> dict:
        if not self.loggedin:
            self.create_session()
        response = self.session.request(method=method,url=url,params=param)
        return response.json()

    @abstractmethod
    def get_addresses(self):
        pass

    @abstractmethod
    def create_addresses(self):
        pass

    @abstractmethod
    def delete_addresses(self):
        pass