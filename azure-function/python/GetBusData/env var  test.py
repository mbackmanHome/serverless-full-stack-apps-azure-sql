import os
import json

with open("local.settings.json", 'r') as config:
    r = config.read()

#print(r.get("values").get("AzureSQLConnectionString"))

out = json.loads(r)

print(out.get("Values").get("AzureSQLConnectionString"))


