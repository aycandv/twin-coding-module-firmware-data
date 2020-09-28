/* V2.1.0 */
#include "src/Twin/Twin.h"

#define _Bluetooth  Serial1
#define _USB        Serial

#define analog      1
#define digital     2

// Giden
// _USB.write(0x95);

// Gelen
// _USB.write(0x98);
      

Channel_st  channel_st;

BOOL        flagBluetooth_b         = false;
BOOL        flagUSB_b               = false;
UINT8       flagGoingByte_u8[2]     = {0};

UINT8       bufferGoingByte_u8[20]  = {0};
UINT8       current_read_status_u8  = sync1_get;
BOOL        flagAnalyzeByte_b       = false;
INT32       temp_i32                = 0;

void setup() {
  _Bluetooth.begin(9600);
  _USB.begin(9600);

  initTwin();
}

void loop() {
  readMessage();
  applyCommands();
  writeMessage();
}
