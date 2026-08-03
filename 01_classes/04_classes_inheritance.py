from pathlib import Path
import logging
import sys
import csv
import ipaddress
import requests
import urllib3

# Disabling ssl warnnings
urllib3.disable_warnings()

# Logging Configuration Level Set
logging.basicConfig(level=logging.INFO)
# Logger declared
logger = logging.getLogger(__name__)

class Firewall:
    def __init__(self, hostname : str, vendor : str, ip : str, username : str, password : str):
        self.hostname = hostname
        self.vendor = vendor
        self.ip = ip
        self.username = username
        self.password = password
        self.login_attempts = 0
        self.logged_in = False
        self.session = False
        self.payload = ""

    def show_info(self):
        logger.info(f"Hostname : {self.hostname}, Vendor : {self.vendor} ,Username : {self.username}, Password : ********")


    def send_request(self, method : str, url : str, payload : str = ""):
        if not self.session:
            raise RuntimeError("Session not created. Call create_session() first")
        try:
            if not payload:
                response = self.session.request(method=method,url=url,timeout=10)
                # Nedd to change this things, because we should able to do any method
                # self.response = self.session.get()
            else:
                response = self.session.request(method=method,url=url,timeout=10,json=payload)
                # Nedd to change this things, because we should able to do any method
                # self.response = self.session.get()
            response.raise_for_status()
            logger.info(f"HTTP : {response.status_code} successful {method}")
            logger.info(response.text)
        except requests.exceptions.ConnectTimeout:
            logger.error("Connection max timeout ...")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Please check the firewall connection")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"Request response not success : {e}")
            raise
        except Exception as e:
            logger.error(f"Error : {e}")
            raise

class Fortigate(Firewall):
    def create_session(self):
        self.session = requests.Session()
        # We should use local variable here
        header = {"Authorization" : f"Bearer {self.password}"}
        self.session.headers.update(header)
        # Verify is not a function
        self.session.verify = False
        self.logged_in = True

    def fgt_get_address(self):
        url = f"https://{self.ip}/api/v2/cmdb/firewall/address"
        self.send_request(method="GET",url=url)

def read_csv_inventory(csv_file : str, vendor_list : list) -> list:
    try:
        firewall_inventory =[]
        if not Path(csv_file).exists():
            raise FileNotFoundError(f"{csv_file} doesn't exsists")
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line, row in enumerate(reader,start=2):
                hostname = row.get("hostname", "").strip()
                vendor = row.get("vendor", "").strip()
                ip = row.get("management_ip","").strip()
                username = row.get("username","").strip()
                password = row.get("password","").strip()
                response = fw_inventory_validator(hostname=hostname,vendor=vendor,ip=ip,username=username,password=password,vendor_li=vendor_list, line_no=line)
                if response.get("error"):
                    logger.debug(response)
                    logger.warning(f"Line {line} : {response.get("message")} is the error. Skipping Line {line}")
                    # raise KeyError(f"Line {line} : {response.get("message")}")
                    continue
                firewall_inventory.append({"hostname":hostname,"vendor":vendor,"ip":ip,"username":username,"password":password})
        return firewall_inventory

    except FileNotFoundError as e:
        logger.error(f"{e}. Exiting")
        sys.exit(1)
    except PermissionError:
        logger.error("File read permission is not present... Exiting...")
        sys.exit(1)
    except KeyError as e:
        logger.warning(e)

def fw_inventory_validator(hostname : str, vendor : str, ip : str, username : str, password : str, vendor_li : list, line_no : int) -> dict:
    response = {"error":True, "message": "Loading..."}
    logger.debug("Inside the inventory")
    if not hostname:
        response["message"]="Hostname is not set"
        return response
    if not vendor in vendor_li:
        response["message"]="Vendor is not in list"
        return response
    try:
        ipaddress.ip_network(ip, strict=False)
    except ValueError:
        response["message"]=f"IP address is not valid {ip}"
        return response
    if not username:
        response["message"]="Username is blank"
        return response
    if not password:
        response["message"]="Password is blank"
        return response
    response = {"error":False, "message": f"All values for line {line_no} is valid"}
    return response


def main():
    fw_vendors = ["FortiGate", "Palo Alto", "Check Point"]
    fw_csv_inventory = "inventory.csv"
    fw_list_inventory = read_csv_inventory(csv_file=fw_csv_inventory, vendor_list=fw_vendors)
    class_firewall = []
    for firewall in fw_list_inventory:
        hostname = firewall.get("hostname")
        vendor = firewall.get("vendor")
        ip = firewall.get("ip")
        username = firewall.get("username")
        password = firewall.get("password")
        fw = Firewall(hostname=hostname,vendor=vendor,ip=ip,username=username,password=password)
        class_firewall.append(fw)
    for firewall in class_firewall:
        Fortigate.create_session(firewall)
        Fortigate.fgt_get_address(firewall)


if __name__ == "__main__":
    main()