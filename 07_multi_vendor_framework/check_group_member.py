def check_group_member(name: str, member:str, address_groups: list) -> dict:
    for group in address_groups:
        if group["name"] == name and member in address_groups["members"]:
            return {"status":False, "message":f"{member} is already present in group {group}"}
        return {"status": True, "message": f"{member} is not present in any group"}