#include <RFduinoBLE.h>

const int TempPin = 2;
const int PulsePin = 3;

volatile int BPM;
volatile int Signal;
volatile int IBI = 600;
volatile boolean Pulse = false;
volatile boolean QS = false;

boolean isConnect;

void setup()
{
  pinMode(TempPin, INPUT);
  pinMode(PulsePin, INPUT);

  Serial.begin(9600);
  Serial.println("Start!");

  RFduinoBLE.deviceName = "smartband";
  RFduinoBLE.begin();
}
    
void loop() // per 1 second
{ 
  // PULSE
  int tm = 0;
  while (tm < 500) {
    getPulse();
    delay(2);
    tm++;

  // TEMP BLE
    if (tm == 250) {
      int val = analogRead(TempPin);
      float temp = (3.0 * val / 1024.0) * 100;

      Serial.print("TEMP: ");
      Serial.println(temp);
          
      RFduinoBLE.sendFloat(temp * -1.0);
    }
  }

  // PULSE BLE
  Serial.print("BPM: ");
  Serial.println(BPM);
    
  RFduinoBLE.sendFloat(BPM * 1.0);
}


/*
  BLE Connection
*/

void RFduinoBLE_onConnect() {
  Serial.println("RFduino connected");
  isConnect = true;
}

void RFduinoBLE_onDisconnect() {
  Serial.println("RFduino disconnected");
  isConnect = false;
}


/*
  Pulse Sensor
*/

volatile int rate[10];                    // array to hold last ten IBI values
volatile unsigned long sampleCounter = 0;          // used to determine pulse timing
volatile unsigned long lastBeatTime = 0;           // used to find IBI
volatile int P = 512;                      // used to find peak in pulse wave, seeded
volatile int T = 512;                     // used to find trough in pulse wave, seeded
volatile int thresh = 530;                // used to find instant moment of heart beat, seeded
volatile int amp = 0;                   // used to hold amplitude of pulse waveform, seeded
volatile boolean firstBeat = true;        // used to seed rate array so we startup with reasonable BPM
volatile boolean secondBeat = false;      // used to seed rate array so we startup with reasonable BPM

void getPulse() {
    Signal = analogRead(PulsePin);              // read the Pulse Sensor
    sampleCounter += 2;                         // keep track of the time in mS with this variable
    int N = sampleCounter - lastBeatTime;       // monitor the time since the last beat to avoid noise
  
    if(Signal < thresh && N > (IBI/5)*3){       // avoid dichrotic noise by waiting 3/5 of last IBI
      if (Signal < T){                        // T is the trough
        T = Signal;                         // keep track of lowest point in pulse wave
      }
    }
  
    if(Signal > thresh && Signal > P){          // thresh condition helps avoid noise
      P = Signal;                             // P is the peak
    }                                        // keep track of highest point in pulse wave
  
    if (N > 250){                                   // avoid high frequency noise
      if ( (Signal > thresh) && (Pulse == false) && (N > (IBI/5)*3) ){
        Pulse = true;                               // set the Pulse flag when we think there is a pulse
        IBI = sampleCounter - lastBeatTime;         // measure time between beats in mS
        lastBeatTime = sampleCounter;               // keep track of time for next pulse
  
        if(secondBeat){                        // if this is the second beat, if secondBeat == TRUE
          secondBeat = false;                  // clear secondBeat flag
          for(int i=0; i<=9; i++){             // seed the running total to get a realisitic BPM at startup
            rate[i] = IBI;
          }
        }
  
        if(firstBeat){                         // if it's the first time we found a beat, if firstBeat == TRUE
          firstBeat = false;                   // clear firstBeat flag
          secondBeat = true;                   // set the second beat flag
          return;                              // IBI value is unreliable so discard it
        }
  
        word runningTotal = 0;                  // clear the runningTotal variable
  
        for(int i=0; i<=8; i++){                // shift data in the rate array
          rate[i] = rate[i+1];                  // and drop the oldest IBI value
          runningTotal += rate[i];              // add up the 9 oldest IBI values
        }
  
        rate[9] = IBI;                          // add the latest IBI to the rate array
        runningTotal += rate[9];                // add the latest IBI to runningTotal
        runningTotal /= 10;                     // average the last 10 IBI values
        BPM = 60000/runningTotal;               // how many beats can fit into a minute? that's BPM!
        QS = true;                              // set Quantified Self flag
      }
    }
  
    if (Signal < thresh && Pulse == true){   // when the values are going down, the beat is over
      Pulse = false;                         // reset the Pulse flag so we can do it again
      amp = P - T;                           // get amplitude of the pulse wave
      thresh = amp/2 + T;                    // set thresh at 50% of the amplitude
      P = thresh;                            // reset these for next time
      T = thresh;
    }
  
    if (N > 2500){                           // if 2.5 seconds go by without a beat
      thresh = 530;                          // set thresh default
      P = 512;                               // set P default
      T = 512;                               // set T default
      lastBeatTime = sampleCounter;          // bring the lastBeatTime up to date
      firstBeat = true;                      // set these to avoid noise
      secondBeat = false;                    // when we get the heartbeat back
    }
}
