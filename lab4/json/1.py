import json
with open(r"C:\KBTU\githowto\PP2\lab4\json\sample-data.json","r",encoding="utf-8") as f:
    d = json.load(f)
print("Interface Status")
print("="*80)
print("{:<50}{:<20}{:<10}{:<10}".format("DN","Description","Speed","MTU"))
print("-"*80)
for i in d["imdata"][:3]:
    attributes = i["l1PhysIf"]["attributes"]
    print("{:<50}{:<20}{:<10}{:<10}".format(

        attributes["dn"],
        attributes.get("descr",""),
        attributes["speed"],
        attributes["mtu"]
        ))