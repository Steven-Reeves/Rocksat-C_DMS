/*
 * Authors:     Andrew Horn, Steven Reeves
 * Modified:    6/1/18
 * Filename:    GeigerV2.ino
 * 
 * Overview:    This code will be used in the 2018 Rocksat-C program for counting the number of times
 *              four different Geiger-Muller tubes are hit with radiation while in space. Three tubes 
 *              are each shielded with different materials, while one is left unshielded for control.
 *              
 *              Each tube is connected to an interrupt, held high and driven low. On the falling edge 
 *              of a signal drop an interrupt method is triggered which increments an intermediate counter,
 *              each tube has its own counter, along with a totalHits counter.
 *              
 *              During the main program loop the intermediate counters are added into the totalHits counters 
 *              and then reset to zero (0). Upon changes in the number of hits, data is printed to a serial
 *              connection and to an SD card in the form of comma-separated values:
 *              
 *                  (int)timestamp,(int)total_number_of_hits,(String)shielding_material
 *                  
 *              This program runs from startup until the Arduino loses power.
 */


/*
 * SD card setup:
 * Unshielded Geiger tube on pin 3
 * FE3O4-shielded Geiger tube on pin 2
 * SRCO3-shielded Geiger tube on pin 7
 * Wax-shielded Geiger tube on pin 0 <- This is the RX pin, but since the Arduino will not be
 *                                      receiving any data over RX/TX or USB during operation 
 *                                      we are safe to use it for the interrupt.
 *                                      
 * Chip select on pin 10, this will activate the SD card breakout board.
 */

#include <SPI.h>
#include <SD.h>


/************* VARIABLE SET UP *************/

#define BAUDRATE          9600  // Serial baudrate
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
bool debug = true;          // Set flag to true for debugging -> produces informative serial statements

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
  // Counter variables are passed by reference in order to modify the global variables.
  
  totalHits += newHits; // Update total hit counter.
  newHits = 0;          // Reset the intermediate counter to zero.

  // Build output string:
  String printOut = String(millis()) + "," + shielding + "," + String(totalHits);
  
  if (serialEnable)
  {
    // If serial port is open, print the message to serial.
    PrintToSerial(printOut);
  }
  if (sdEnable)
  {
    // If the SD card is initialized, write the message to the SD card.
    WriteToSD(printOut);
  }
}

/************* PRINT FUNCTIONS *************/

// Write printMe string to the serial port.
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
    // If the file is open, write the writeMe string and close the file.
    dataFile.println(writeMe);
    dataFile.close();
  }
  else
  {
    if (serialEnable && debug)
    {
      // If the file is not open, the serial port is open, and debug mode is on, print a failure message.
      Serial.println("Unable to write to SD card.");  
    }
  }
}

/************* INITIALIZATION FUNCTIONS *************/

// Initialize the SD card
void InitSd()
{
  short i = 0;
  pinMode(chipSelect, OUTPUT); // Chip select pin must be set as an output, even if not being used.
  while (!SD.begin(SS) && i++ < 100) { delay(10); } // Try to initialize SD card for up to 1 second.
  // The above line may need to be removed, we should only have to attempt to open and initialize the 
  // SD card once. 

  // Can also try using SD.begin(SS, SPI_HALF_SPEED), this helps connect to older, slower, or larger cards.
  if (SD.begin(SS)) // Use "SS" instead of chipSelect, default value helps when not connected to USB.
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
  while (!Serial && i++ < 10) 
    { 
      Serial.begin(BAUDRATE);
      delay(100);      
    } // Try to open the serial port for up to 1 second.

  if(Serial)
  {
    // If the port opened successfully, set the flag appropriately. <- This may be unneccessary,
    // we could just check for Serial instead of the serialEnable flag, but I'm unsure of how this
    // could affect the connection. Sticking with the serialEnable flag for safety.
    serialEnable = true;
    if (debug)
    {
      // If debug mode is on, print the serial status.
      Serial.println("Serial open! serialEnable set to true");
    }
  }
}

/************* INTERRUPT FUNCTIONS *************/
// Interrupt functions cannot take parameters nor return values,
// this is why the counters are global variables.

void TubeOne() { tubeOneHits++; }

void TubeTwo() { tubeTwoHits++; }

void TubeThree() { tubeThreeHits++; }

void TubeFour() { tubeFourHits++; }
