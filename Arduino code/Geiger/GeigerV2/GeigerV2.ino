#include <SPI.h>
#include <SD.h>

/************* VARIABLE SET UP *************/

const short chipSelect = 10;      // Actual pin 10
const short tubeOneIntPin = 3;    // unshielded
const short tubeTwoIntPin = 2;    // FE3O4
const short tubeThreeIntPin = 7;  // SRCO3
const short tubeFourIntPin = 0;   // WAX


unsigned int tubeOneHits = 0;     // Used to count intermediate hits
unsigned long tubeOneTotal = 0;   // Used to count total number of hits
unsigned int tubeTwoHits = 0;     // Used to count intermediate hits
unsigned long tubeTwoTotal = 0;   // Used to count total number of hits
unsigned int tubeThreeHits = 0;   // Used to count intermediate hits
unsigned long tubeThreeTotal = 0; // Used to count total number of hits
unsigned int tubeFourHits = 0;    // Used to count intermediate hits
unsigned long tubeFourTotal = 0;  // Used to count total number of hits

bool sdEnable = false;      // Flag set to true when SD card successfully initialized
bool serialEnable = false;  // Flag set to true when Serial port successfully opened
bool debug = false;         // Flag set to true for debugging -> produces more serial statements

unsigned long timestamp = 0;  // Used to hold timestamp value (ms since boot)

String printOut = ""; // Used to hold string to be printed to Serial and/or written to SD card



void setup() 
{

  /******** INITIALIZATION ********/
  // Both initialization functions set a flag upon success, all statements that 
  // print to serial or write to the SD check for the flag before executing,
  // eliminating errors when either one isn't functioning correctly.
  
  InitSerial(); // Initialize serial output, used to send data to Raspberry Pi
  InitSd();     // Initialize SD card for local data storage
  /********************************/

  /******** INTERRUPT SETUP ********/
  // Interrupt pins must be set with the internal pullup resistors activated, otherwise
  // the interrupts are triggered by electrical noise, nullifying all results.
  pinMode(tubeOneIntPin, INPUT_PULLUP);
  pinMode(tubeTwoIntPin, INPUT_PULLUP);
  pinMode(tubeThreeIntPin, INPUT_PULLUP);
  pinMode(tubeFourIntPin, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(tubeOneIntPin), TubeOne, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeTwoIntPin), TubeTwo, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeThreeIntPin), TubeThree, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeFourIntPin), TubeFour, RISING);
  /*********************************/

  // debug printout
  if (serialEnable && debug)
  {
    Serial.println("Setup complete!");  
  }
}


void loop() {
  if (tubeOneHits > 0)
  {
    tubeOneTotal += tubeOneHits;
    tubeOneHits = 0;
    timestamp = millis();
    printOut = String(timestamp) + ",unshielded," + String(tubeOneTotal);
    if (serialEnable)
    {
      PrintToSerial(printOut);  
    }
    if (sdEnable)
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
    if (serialEnable)
    {
      PrintToSerial(printOut);  
    }
    if (sdEnable)
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
    if (serialEnable)
    {
      PrintToSerial(printOut);  
    }
    if (sdEnable)
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
    if (serialEnable)
    {
      PrintToSerial(printOut);  
    }
    if (sdEnable)
    {
      WriteToSD(printOut);
    }
    //UpdateCount(tubeFourTotal, tubeFourHits, "wax");
  }
}

/************* OUTPUT FUNCTIONS *************/

void UpdateCount(unsigned long &totalHits, unsigned long &newHits, String shielding)
{
  totalHits += newHits;
  newHits = 0;
  timestamp = millis();
  printOut = String(millis()) + "," + shielding + "," + String(totalHits);
  if (serialEnable)
  {
    PrintToSerial(printOut);
  }
  if (sdEnable)
  {
    WriteToSD(printOut);
  }
}
/************* PRINT FUNCTIONS *************/
void PrintToSerial(String printMe)
{
  if (serialEnable)
  {
    Serial.println(printMe); 
  }
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
    if (serialEnable && debug)
    {
      Serial.println("Unable to write to SD card.");  
    }
  }
}


/************* INITIALIZATION FUNCTIONS *************/
void InitSd()
{
  short i = 0;
  while (!SD.begin(chipSelect) && i < 100)
  {
    i++;
    delay(10);
    // try to initialize card before giving up
  }
  if (!SD.begin(chipSelect))
  {
    if (serialEnable && debug)
    {
      Serial.println("Failed to initialize SD card.");  
    }
  }
  else
  {
    if (serialEnable && debug)
    {
      Serial.println("SD Card initialized!");  
    }
    sdEnable = true;
  }
}

void InitSerial()
{
  short i = 0;
  Serial.begin(57600);
  while (!Serial && i < 100)
  {
    i++;
    delay(10);
    // try to connect for 1 second before giving up
  }
  if(Serial)
  {
    serialEnable = true;
    if (debug)
    {
      Serial.println("Serial open! serialEnable set to true");
    }
  }
}


/************* INTERRUPT FUNCTIONS *************/

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
