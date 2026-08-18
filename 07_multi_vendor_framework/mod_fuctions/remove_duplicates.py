def remove_duplicates(new_address, exsiting_address):
    exsiting_names = []
    exsiting_ips = []
    unique_entry = []
    duplicate_entry = []
    for item in exsiting_address:
        exsiting_names.append(item.get("name"))
        exsiting_ips.append(item.get("ip"))
    for item in new_address:
        if item.get("name") in set(exsiting_names):
            item["status"] = "NA"
            item["confirm"] = "Duplicate"
            duplicate_entry.append(item)
            continue
        if item.get("ip") in set(exsiting_ips):
            item["status"] = "NA"
            item["confirm"] = "Duplicate"
            duplicate_entry.append(item)
            continue
        unique_entry.append(item)
    return {"unique":unique_entry,"dups":duplicate_entry}