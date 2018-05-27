#include <SPI.h>
#include <SD.h>

const short chipSelect = 10;
const short tubeOneIntPin = 3; // unshielded
const short tubeTwoIntPin = 2; // FE3O4
const short tubeThreeIntPin = 7; // SRCO3
const short tubeFourIntPin = 0; // This is the RX pin. WAX
short SdEnable = 0;
short SerialEnable = 1;

unsigned int tubeOneHits = 0;
unsigned long tubeOneTotal = 0;
unsigned int tubeTwoHits = 0;
unsigned long tubeTwoTotal = 0;
unsigned int tubeThreeHits = 0;
unsigned long tubeThreeTotal = 0;
unsigned int tubeFourHits = 0;
unsigned long tubeFourTotal = 0;

unsigned long testOut = 0;
unsigned long timestamp = 0;

String printOut = "";

void TubeOne()
{
  tubeOneHits++;
}

void TubeTwo()
{
  tubeTwoHits++;
}

void TubeThree()
{
  tubeThreeHits++;
}

void TubeFour()
{
  tubeFourHits++;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  short i = 0;
  while (!Serial && i < 1000)
  {
    i++;
  }
  if(!Serial)
  {
    SerialEnable = 0;
  }
  pinMode(chipSelect, OUTPUT);
  delay(10);
  while (!SD.begin(chipSelect))
  {
    Serial.println("Failed to initialize SD card.");
  }
    Serial.println("SD Card initialized!");
    SdEnable = 1;
  
  pinMode(tubeOneIntPin, INPUT_PULLUP);
  pinMode(tubeTwoIntPin, INPUT_PULLUP);
  pinMode(tubeThreeIntPin, INPUT_PULLUP);
  pinMode(tubeFourIntPin, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(tubeOneIntPin), TubeOne, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeTwoIntPin), TubeTwo, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeThreeIntPin), TubeThree, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeFourIntPin), TubeFour, RISING);
  Serial.println("Setup complete!");
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

    if (tubeOneHits > 0)
    {
      tubeOneTotal += tubeOneHits;
      tubeOneHits = 0;
      timestamp = millis();
      printOut = String(timestamp) + ",unshielded," + String(tubeOneTotal);
      PrintToSerial(printOut);
      if (SdEnable)
      {
        WriteToSD(printOut);
      } 
    }
    if (tubeTwoHits > 0)
    {
      tubeTwoTotal += tubeTwoHits;
      tubeTwoHits = 0;
      timestamp = millis();
      printOut = String(timestamp) + ",fe3o4," + String(tubeTwoTotal);
      PrintToSerial(printOut);
      if (SdEnable)
      {
        WriteToSD(printOut);
      }
    }
    if (tubeThreeHits > 0)
    {
      tubeThreeTotal += tubeThreeHits;
      tubeThreeHits = 0;
      timestamp = millis();
      printOut = String(timestamp) + ",srco3," + String(tubeThreeTotal);
      PrintToSerial(printOut);
      if (SdEnable)
      {
        WriteToSD(printOut);
      }
    }
    if (tubeFourHits > 0)
    {
      tubeFourTotal += tubeFourHits;
      tubeFourHits = 0;
      timestamp = millis();
      printOut = String(timestamp) + ",wax," + String(tubeFourTotal);
      PrintToSerial(printOut);
      if (SdEnable)
      {
        WriteToSD(printOut);
      }
    }

    /* For Debugging: */
   // testOut++;
   // if (testOut > 500000)
   // {
   //   Serial.println("Running...");
   //   testOut = 0;
   // }
}

void PrintToSerial(String printMe)
{
  Serial.println(printMe);
}

void WriteToSD(String writeMe)
{
  File dataFile = SD.open("geiger.txt", FILE_WRITE);
  if (dataFile)
  {
    dataFile.println(writeMe);
    dataFile.close();
  }
  else
  {
    Serial.println("Unable to write to SD card.");
  }
}

