import serial.tools.list_ports as port_list     # first, pip install pyserial
import os
import requests
from update_check import isUpToDate, update


def check_network_conection():
    try:
        _ = requests.get("http://www.google.com", timeout=4)
        return True
    except requests.ConnectionError:
        print("There is no Internet connection...")
    return False

def check_github_repo_updates():
    username = "aycandv"
    repo = "/twin-coding-module-firmware-data/master/"
    _dir = "TwinArduinoFirmware/"

    files = [i for i in os.listdir("TwinArduinoFirmware") if i.endswith(".ino")]

    for i in files:
        if isUpToDate(_dir + i, "https://raw.githubusercontent.com/"+ username + repo + _dir + i) == False:
            print("====>", i,"is not up to date")
            update(_dir + i, "https://raw.githubusercontent.com/"+ username + repo + _dir + i)
            print("====>", i, "is updated")
        else:
            print("====>", i,"is up to date")

def check_for_updates():
    if check_network_conection() is True:
        print("Connection established")
        check_github_repo_updates()
    else:
        print("Offline mode")

def detect_port():
    ports = list(port_list.comports())
    for p in ports:
        if "Arduino Leonardo" in p:
            port_name = str(p).split(" ")
            return port_name[0]
    raise IOError("Twin Coding Module is not found...")

def upload_firmware():
    process = os.system("./arduino-cli upload --port " + str(detect_port()) + " --fqbn arduino:avr:leonardo TwinArduinoFirmware/TwinArduinoFirmware.ino > /dev/null 2>&1")
    if process == 0:
        print("Software update is successful")
    else:
        print("Software update is failed")
    return process


if __name__ == "__main__":
    #check_for_updates()
    #upload_firmware()
    print(os.name)