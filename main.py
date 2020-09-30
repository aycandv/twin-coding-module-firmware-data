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
    dir_output = "TwinArduinoFirmware/build/arduino.avr.leonardo/"

    files_ino = [i for i in os.listdir(dir_ino) if i.endswith(".ino")]
    files_output = [i for i in os.listdir(dir_output) if i.endswith(".hex")]

    for i in files_ino:
        if isUpToDate(dir_ino + i, "https://raw.github.com/"+ username + repo + dir_ino + i) == False:
            print("====>", i,"is not up to date")
            update(dir_ino + i, "https://raw.github.com/"+ username + repo + dir_ino + i)
            print("====>", i, "is updated")
        else:
            print("====>", i,"is up to date")

    for i in files_output:
        if isUpToDate(dir_output + i, "https://raw.github.com/"+ username + repo + dir_output + i) == False:
            print("====>", i,"is not up to date")
            update(dir_output + i, "https://raw.github.com/"+ username + repo + dir_output + i)
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
    print(detect_port()[-1])
    #check_for_updates()
    #cli_setup()
    upload_firmware()
