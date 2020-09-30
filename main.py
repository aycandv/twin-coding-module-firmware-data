import serial.tools.list_ports as port_list     # first, pip install pyserial
import os
import time
import requests                                 # pip install requests
from update_check import isUpToDate, update     # pip install update-check


def check_network_conection():
    try:
        _ = requests.get("http://www.google.com", timeout=4)
        return True
    except requests.ConnectionError:
        print("There is no Internet connection...")
    return False


def check_github_repo_updates():
    username = "aycandv/"
    repo = "twin-coding-module-firmware-data/master/"
    dir_ino = "TwinArduinoFirmware/"

    files_output = [i for i in os.listdir() if i.endswith(".hex")]

    for i in files_output:
        if isUpToDate(i, "https://raw.github.com/"+ username + repo + i) == False:
            print("====>", i,"is not up to date")
            update(i, "https://raw.github.com/"+ username + repo + i)
            print("====>", i, "is updated")
        else:
            print("====>", i,"is up to date")


def check_for_updates():
    if check_network_conection() is True:
        print("Internet Connection is established")
        check_github_repo_updates()
    else:
        print("Offline mode")


def detect_port():
    ports = list(port_list.comports())
    if os.name == "nt":
        for p in ports:
            print(p)
            if "USB" in str(p) or "Arduino Leonardo" in str(p):
                return p.device
    elif os.name == "posix":
        for p in ports:
            if "Arduino Leonardo" in str(p):
                return p.device
    raise IOError("Twin Coding Module is not found...")


def cli_setup():
    if os.name == "posix":
        os.system("./arduino-cli core install arduino:avr")
        os.system("./arduino-cli core update-index")
        os.system('./arduino-cli lib install "Servo"')
        os.system("./arduino-cli lib update-index")
    elif os.name == "nt":
        os.system("arduino-cli core install arduino:avr")
        os.system("arduino-cli core update-index")
        os.system('arduino-cli lib install "Servo"')
        os.system("arduino-cli lib update-index")


def upload_firmware():
    if os.name == "posix":
        process = os.system("./arduino-cli upload --port " + str(detect_port()) + " -i TwinArduinoFirmware.ino.hex --fqbn arduino:avr:leonardo > /dev/null 2>&1")
    elif os.name == "nt":
        process = os.system("arduino-cli upload --port " + str(detect_port()) + " -i TwinArduinoFirmware.ino.hex --fqbn arduino:avr:leonardo")
    if process == 0:
        print("Success")
    else:
        print("Failed")


if __name__ == "__main__":
    # These two lines below, run while loading app screen
    check_for_updates()
    cli_setup()
    # After clicking Upload Button, below line of code runs. For Windows, users should push reset button once
    # after clicking "Upload" button. There is nothing to do for macOS.
    upload_firmware()
