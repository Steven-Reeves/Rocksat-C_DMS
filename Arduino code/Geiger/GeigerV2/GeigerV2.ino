#include <SPI.h>
#include <SD.h>

/************* VARIABLE SET UP *************/

#define BAUDRATE          9600 // Serial baudrate
#define chipSelect        10    // Chip select pin for SD card
#define tubeOneIntPin     3     // Unshielded tube
#define tubeTwoIntPin     2     // FE3O4 shielded tube
#define tubeThreeIntPin   7     // SRCO3 shielded tube
#define tubeFourIntPin    0     // Wax shielded tube

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
bool debug = false;         // Set flag to true for debugging -> produces more serial statements

void setup() 
{

  /******** INITIALIZATION ********/
  // Both initialization functions set a flag upon success, all statements that 
  // print to serial or write to the SD check for the flag before executing,
  // eliminating errors when either one isn't functioning correctly.
  
  InitSerial(); // Initialize serial output, used to send data to Raspberry Pi.
  InitSd();     // Initialize SD card for local data storage.
  
  /********************************/

  /******** INTERRUPT SETUP ********/
  // Interrupt pins must be set with the internal pullup resistors activated, otherwise
  // the interrupts are triggered by electrical noise, effectively nullifying all results.
  pinMode(tubeOneIntPin, INPUT_PULLUP);
  pinMode(tubeTwoIntPin, INPUT_PULLUP);
  pinMode(tubeThreeIntPin, INPUT_PULLUP);
  pinMode(tubeFourIntPin, INPUT_PULLUP);

  // Call interrupt methods on RISING edge of signal.
  attachInterrupt(digitalPinToInterrupt(tubeOneIntPin), TubeOne, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeTwoIntPin), TubeTwo, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeThreeIntPin), TubeThree, RISING);
  attachInterrupt(digitalPinToInterrupt(tubeFourIntPin), TubeFour, RISING);
  /*********************************/

  // Debug printout.
  if (serialEnable && debug)
  {
    Serial.println("Setup complete!");  
  }
}

void loop() {
  
  // Main loop of program will run anytime there are no interrupt methods on
  // the call stack. It will check each tube's intermediate hit counter and 
  // print the appropriate information when there are changes.
    
  if (tubeOneHits > 0)
  {
    UpdateCount(tubeOneTotal, tubeOneHits, "unshielded");
  }
  if (tubeTwoHits > 0)
  {
    UpdateCount(tubeTwoTotal, tubeTwoHits, "fe3o4");
  }
  if (tubeThreeHits > 0)
  {
    UpdateCount(tubeThreeTotal, tubeThreeHits, "src03");
  }
  if (tubeFourHits > 0)
  {
    UpdateCount(tubeFourTotal, tubeFourHits, "wax");
  }
}

/************* OUTPUT FUNCTIONS *************/

void UpdateCount(unsigned long & totalHits, unsigned int & newHits, String shielding)
{
  // Counter variables are passed by reference in order to update/manipulate the global variables.
  
  totalHits += newHits; // Update total hit counter with new additions.
  newHits = 0;          // Reset the intermediate counter to zero.

  // Build output string:
  String printOut = String(millis()) + "," + shielding + "," + String(totalHits);
  
  if (serialEnable)
  {
    // Ff serial port is open, print the message to serial.
    PrintToSerial(printOut);
  }
  if (sdEnable)
  {
    // If the SD card is initialized, write the message to the SD card.
    WriteToSD(printOut);
  }
}

/************* PRINT FUNCTIONS *************/

// Write string to serial port
void PrintToSerial(String &printMe)
{
  if (serialEnable)
  {
    // If the serial port is open, print the message.
    // This should be checked before calling this method,
    // but to be safe it is checked here as well.
    Serial.println(printMe); 
  }
}

// Write string to SD card
void WriteToSD(String &writeMe)
{
  File dataFile = SD.open("geiger.txt", FILE_WRITE); // open data file
  if (dataFile)
  {
    // If the file is open, write data and close the file.
    dataFile.println(writeMe);
    dataFile.close();
  }
  else
  {
    if (serialEnable && debug)
    {
      // If the serial port is open and debug mode is on, print a failure message.
      Serial.println("Unable to write to SD card.");  
    }
  }
}

/************* INITIALIZATION FUNCTIONS *************/

// Initialize SD card
void InitSd()
{
  short i = 0;
  while (!SD.begin(chipSelect) && i++ < 100) { delay(10); } // Try to initialize SD card for up to 1 second.
  
  if (SD.begin(chipSelect))
  {
    // If the SD card is initialized, set the flag appropriately.
    sdEnable = true;
    
    if (serialEnable && debug)
    {
      // If the serial port is open and debug mode is on, print the SD card status.
      Serial.println("SD card initialized successfully.");
    }
  }
  else
  {
    if (serialEnable && debug)
    {
      // If the serial port is open and debug mode is on, print a failure message.
      Serial.println("Failed to initialize SD card.");  
    }
  }
}

// Initializes the serial port
void InitSerial()
{
  short i = 0;
  //Serial.begin(BAUDRATE);
  while (!Serial && i++ < 10) 
    { 
      Serial.begin(BAUDRATE);
      delay(100);      
    } // Try to open the serial port for up to 1 second.

  if(Serial)
  {
    // If the port opened successfully, set the flag appropriately.
    serialEnable = true;
    if (debug)
    {
      // If debug mode is on, print the serial status.
      Serial.println("Serial open! serialEnable set to true");
    }
  }
}

/************* INTERRUPT FUNCTIONS *************/

void TubeOne() { tubeOneHits++; }

void TubeTwo() { tubeTwoHits++; }

void TubeThree() { tubeThreeHits++; }

void TubeFour() { tubeFourHits++; }
