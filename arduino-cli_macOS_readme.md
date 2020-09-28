# Arduino-CLI for macOS/Linux
## Setup
1. `curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh`
2. `./arduino-cli core update-index`
3. `./arduino-cli core search leonardo`
4. `./arduino-cli core install arduino:avr`

## Verification
1. `./arduino-cli core list`
2. `./arduino-cli board listall`
3. `./arduino-cli board list` (List of connected boards)

## Install Third-Party Libraries
1. `./arduino-cli lib update-index`
2. `./arduino-cli lib search Servo`
3. `./arduino-cli lib install "Adafruit NeoPixel" `(or "Servo")
4. `./arduino-cli lib list`

## Compilation 
1. [Follow this guide.](https://www.devdungeon.com/content/arduino-cli-tutorial)
2. An example of the usage
    ```
    ./arduino-cli compile --fqbn arduino:avr:leonardo TwinArduinoFirmware/TwinArduinoFirmware.ino 
    ./arduino-cli upload --port /dev/cu.usbmodem141101 --fqbn arduino:avr:leonardo TwinArduinoFirmware/TwinArduinoFirmware.ino
    ```
