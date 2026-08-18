from logging_basic_config import logging_basic_config
import logging
from paloalto import PaloAlto
from fortigate import Fortigate
import urllib3
from mod_fuctions.trim_functions.trim_addresses import get_exsiting_address
from mod_fuctions.trim_functions.trim_groups import get_address_groups
from mod_fuctions import read_csv
from mod_fuctions.remove_duplicates import remove_duplicates
from check_group_member import check_group_member
urllib3.disable_warnings()

logging_basic_config()
logger = logging.getLogger(__name__)

def main():
    csv_file = "address.csv"
    fortigate = Fortigate(hostname="FGT-HQ",vendor="FortiGate",username="admin",ip="192.168.35.249",key="h36bGs4p5rpcmNwf8dw7Hrs5Qq50hQ")
    # paloalto = PaloAlto(hostname="PA-HQ",vendor="PaloAlto",username="admin",ip="192.168.35.248",key="LUFRPT0zVTZKMldwdE5qd21DeWVtaG5vZGFQT3pjS0U9bkJodVJ5VDVQanJDdVVYNFFPbm5MNFdoL0R6TkltU2cvVDNsa0FpWjZhb2xweUt1T1lPdmhUbkJPbTVyVGQ3dA==")
    # firewalls = [fortigate,paloalto]
    new_address = read_csv.read_csv(csv_file=csv_file)
    firewalls = [fortigate]
    for firewall in firewalls:
        # firewall.show_info()
        firewall.create_session()
        addresses = firewall.get_addresses()
        exsiting_fqdns, exsiting_ips = get_exsiting_address(addresses)
        address_groups = firewall.get_address_group()
        exsiting_addr_groups = get_address_groups(address_groups)
        # I know right now I am not implementing the unique addrgrps
        ips_result = remove_duplicates(new_address=new_address,exsiting_address=exsiting_ips)
        unique_entry = ips_result.get("unique")
        duplicate_entry = ips_result.get("dups")
        if len(unique_entry) != 0:
            for entry in unique_entry:
                payload = {"name":entry["name"],"subnet":entry["ip"],"type":"ipmask"}
                result = firewall.create_addresses(payload=payload)
                print(result.get("status"))
                entry["status"] = result.get("status")
                verify_addresses = firewall.get_addresses()
                for address in verify_addresses:
                    if address["name"] == entry["name"]:
                        entry["confirm"] = "Verfied"
        else:
            print("Everything is duplicate only")
        complete_entry = unique_entry + duplicate_entry
        print(complete_entry)
        new_groups = {"name": "CCU-Calcut", "member":[{"name": "CCU_LAN_INTERNAL"}]}
        member=new_groups["member"]
        member=member[0]["name"]
        addrgrps_result = check_group_member(name=new_groups["name"],member=new_groups["member"][0]["name"],address_groups=exsiting_addr_groups)
        print(addrgrps_result["message"])
        if addrgrps_result["status"]:
            result = firewall.create_address_group(payload=new_groups)
            print(result)
            print(result["status"])
            stat = result.get("status")
            new_groups["status"]=stat
            verify_addrgrps = firewall.get_address_group()
            for address in verify_addrgrps:
                if address["name"] == new_groups["name"]:
                    new_groups["confirm"] = "Verfied"
        print(new_groups)

if __name__ == "__main__":
    main()