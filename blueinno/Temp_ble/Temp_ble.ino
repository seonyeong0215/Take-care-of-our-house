#include <RFduinoBLE.h>

const int TempPin = 2;
boolean isConnect;

void setup()
{
  pinMode(TempPin, INPUT);

  RFduinoBLE.deviceName = "smartband";

  Serial.begin(9600);
  Serial.println("Start Test");

  RFduinoBLE.begin();
}
    
void loop()
{ 
  RFduino_ULPDelay(SECONDS(1));

  if (isConnect) {
    int val = analogRead(TempPin);
    float temp = (3.0*val/1024.0)*100;

    Serial.println(temp);

    RFduinoBLE.sendFloat(temp);
  }
}

void RFduinoBLE_onConnect() {
  Serial.println("RFduino connected");
  isConnect = true;
}

void RFduinoBLE_onDisconnect() {
  Serial.println("RFduino disconnected");
  isConnect = false;
}
