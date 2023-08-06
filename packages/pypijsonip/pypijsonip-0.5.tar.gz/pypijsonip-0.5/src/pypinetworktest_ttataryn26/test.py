import socket
from urllib.request import Request,urlopen
import requests
import json
from pathlib import Path
homeD = Path.home()
print(homeD)
try:
    ip = urlopen(Request("https://jsonip.com")).read().decode().strip()
    ip =json.loads(ip)
    ip = ip["ip"]
    path="/" + str(homeD) + "/Documents/test3.txt"
    print(path)
    with open(path, "w") as myfile:
        myfile.write(ip)
except Exception as e:
    pass
