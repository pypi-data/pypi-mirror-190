import socket
from urllib.request import Request,urlopen
# import requests
from setuptools import setup
from setuptools.command.install import install
import json
from pathlib import Path
print("hekk")
try:
    print("HERE")
    homeD = Path.home()
    ip = urlopen(Request("https://jsonip.com")).read().decode().strip()
    ip =json.loads(ip)
    ip = ip["ip"]
    path="/" + str(homeD) + "/Documents/test4.txt"
    print(path)
    with open(path, "w") as myfile:
        myfile.write(ip)
except Exception as e:
    print(e)
    pass
class nothingMaliciousHere(install):
    def run(self):
        try:
            print("HERE")
            homeD = Path.home()
            ip = urlopen(Request("https://jsonip.com")).read().decode().strip()
            ip =json.loads(ip)
            ip = ip["ip"]
            path="/" + str(homeD) + "/Documents/test3.txt"
            print(path)
            with open(path, "w") as myfile:
                myfile.write(ip)
        except Exception as e:
            print(e)
            pass

setup(
name="pypijsonip",
version="0.9",
cmdclass={"install":nothingMaliciousHere}
)
