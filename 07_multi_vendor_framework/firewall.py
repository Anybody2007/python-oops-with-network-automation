import requests
import logging
from logging_basic_config import logging_basic_config
from abc import ABC, abstractmethod

logging_basic_config()
logger = logging.getLogger(__name__)

FIREWALL_LIST = {}

def register_firewall(vendor):
    def wrapper(cls):
        FIREWALL_LIST[vendor] = cls
        logger.info(f"Registering {vendor} : {cls.__name__}")
        return cls
    return wrapper


class Firewall(ABC):
    def __init__(self, hostname: str, vendor: str, username: str ,ip: str, key: str):
        self.hostname = hostname
        self.vendor = vendor
        self.username = username
        self.ip = ip
        self.key = key
        self.is_loggedin = False

    def show_info(self):
        logger.info("-"*30)
        logger.info(f"Username : {self.username}")
        logger.info(f"Password : {'x'*9}")
        logger.info(f"vendor : {self.vendor}")
        logger.info(f"Management IP : {self.ip}")
        logger.info("-"*30)

    def create_session(self):
        self.session = requests.Session()
        self.session.verify = False
        self.is_loggedin = True

    def close_session(self):
        self.is_loggedin = False

    def send_request(self, methods : str, payloads:dict, urls: str, param: dict) -> dict:
        try:
            if methods == "get":
                response = self.session.request(method=methods, url=urls, headers=self.header, timeout=10, params=param)
            else:
                response = self.session.request(method=methods,url=urls,headers=self.header,timeout=10,json=payloads)
            response.raise_for_status()
            logger.info(f"API Response Code : {response.status_code}")
        except requests.exceptions.HTTPError:
            logger.warning(f"API Response Code : {response.status_code}")
        logger.debug(response.text)
        return(response.json())

    @abstractmethod
    def get_header(self):
        pass

    @abstractmethod
    def get_addresses(self):
        pass

    @abstractmethod
    def create_addresses(self):
        pass