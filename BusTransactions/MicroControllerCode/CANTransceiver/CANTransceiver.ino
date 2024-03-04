#include <CAN.h> // default clock-frequency needs to be set to 8k

const int maxCAN_MessageLength = 64;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("CAN Receiver");
  // start the CAN bus at 500 kbps
  if (!CAN.begin(500E3)) {
    Serial.println("Starting CAN failed!");
    while (1);
  }
}
void loop() {
  /*
  Main-program structuring and managing all functions
  */
  if (Serial.available() > 0)
  {
    readSerialData();
  }
  receiveCAN_Message();
}

void receiveCAN_Message() {
  // try to parse packet
  int packetSize = CAN.parsePacket();
  char can_message[packetSize];
  if (CAN.packetRtr()) 
  {
    // Remote transmission request, packet contains no data
    // No data is no necessary information so quitting the transmission
    return;
  }
  //Start-byte
  can_message[1] = CAN.packetId();
  int counter = 1;
  while (CAN.available()) {
    can_message[counter] = CAN.read();
    counter ++;
    }
    //End-byte
  sendSerialData(can_message, packetSize);
}

void sendSerialData(char serialData[maxCAN_MessageLength], int packetSize) {
  /*
  Function for sending Serial messages to computer.
  Sending a single byte of data on each iteration with an end-byte: '&',
  marking the end of data and transmission.
  */
  for (int counter=0; counter++; counter <= sizeof(packetSize)){
    Serial.print(serialData[counter]);
  }
  //Sending message end-byte
  Serial.print('&');
}

void readSerialData(){
  /*
  Function for reading Serial messages from computer.
  Reading a single byte of data on each iteration until end-byte '&',
  has been read which marks the end of transmission.
  */
  char serialData[maxCAN_MessageLength];
  int counter = 0;
  if (Serial.available() > 0)
  {
    while (serialData != '&');
    {
        //Reading a single byte on every iteration and 
        //adding that up to an array.
        serialData[counter] = Serial.read();
        counter ++;
    }
  } 
  sendCAN_Message(serialData);
}

void sendCAN_Message(char serialData[maxCAN_MessageLength]) {
  /*
  Sending the CAN-message received from computer to the car!
  */
  //Starting CAN-Message with ID
  CAN.beginPacket(serialData);
  for (int counter=0; counter++; counter <= sizeof(serialData))
  {
    //writing the data-fields
    CAN.write(serialData[counter]);
  }
  //sending message-end
  CAN.endPacket();
}

