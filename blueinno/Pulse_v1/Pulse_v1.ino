#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Serial.println("START");
  Wire.begin();
}

void loop() {
  Wire.requestFrom(0xA0 >> 1, 1);

  Serial.print(Wire.available());
  Serial.print(" , ");
  
  while (Wire.available()) {
    unsigned char c = Wire.read();    
    Serial.println(c, DEC);
  }

  delay(1000);
}
