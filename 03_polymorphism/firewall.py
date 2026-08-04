from logging_basic_config import logging_basic_config
import requests

logger = logging_basic_config()

class Firewall():
    def __init__(self, key: str, ip: str, vendor: str):
        self.ip = ip
        self.key = key
        self.vendor = vendor
        self.loggedin = True

    def show_info(self):
        logger.info(f"Key : {'*'*20}")
        logger.info(f"IP : {self.ip}")
        logger.info(f"Vendor : {self.vendor}")
        logger.info(f"Logged In : {self.loggedin}")

    def create_session(self):
        self.session = requests.Session()
        self.session.verify = False
        self.loggedin = True

    def close_session(self):
        self.session.close()
        self.loggedin = False

    def send_request(self,method: str , url: str, param: dict = None) -> dict:
        if not self.loggedin:
            logger.warning("No session is created, creating session")
            self.create_session()
        response = self.session.request(method=method,url=url,params=param)
        return response.json()