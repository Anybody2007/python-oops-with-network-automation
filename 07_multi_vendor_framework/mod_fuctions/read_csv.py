from logging_basic_config import logging_basic_config
import logging
from pathlib import Path
import csv
import ipaddress

logger = logging.getLogger(__name__)

def read_csv(csv_file: str) -> dict:
    try:
        if not Path(csv_file).exists():
            raise FileNotFoundError(f"{csv_file} : File Not Found")
        if not Path(csv_file).is_file():
            raise FileNotFoundError(f"{csv_file} : Is not a valid file")
        csv_address = []
        with open(file=csv_file, mode="r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for line_no,item in enumerate(reader,start=2):
                name = item.get("name", "")
                ip = item.get("ip", "")
                result = validate_ip_name(ip=ip,name=name,line_no=line_no)
                if not result["status"]:
                    logger.info(result["message"])
                    continue
                logger.debug(result["message"])
                csv_address.append(item)
        return csv_address
    except PermissionError:
        raise PermissionError(f"{csv_file} : Don't have permission")

def validate_ip_name(ip: str, name: str, line_no: str) -> dict:
    result = {"status":False,"message":"Function yet to run"}
    if not name:
        result["message"]=f"{line_no} : Name not valid"
        return result
    try:
        ipaddress.IPv4Network(ip, strict=False)
    except:
        result["message"]=f"{line_no} : IP is not valid"
        return result
    result = {"status":True,"message":f"{line_no} : Name {name} and IP {ip} is valid entry"}
    return result
