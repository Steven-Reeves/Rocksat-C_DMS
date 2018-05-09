/*
 * Author:  Andy Horn
 * Date:    5/2/18
 * 
 * Geiger-Muller radiation detection on an Arduino Micro for Rocksat-C 2017.
 * Set up for 4 GM tubes to write to an SD card with the total number of hits for each tube,
 * along with sending the count out on the serial port.
 * 
 * Interrupt pins: 0 (RX), 1 (TX), 2, 3, 7
 * We will use the RX and TX pins as interrupts since all serial communication will take place through the USB port.
 */

  #include <SPI.h>
  #include <SD.h> // include the SD card library
  // Using unsigned longs to maximize counting range ( 0 - 4,294,967,295)
  unsigned long timestamp; // Counted in hundredths of a second, this will give us nearly 500 days.
  unsigned long tube_one_hits;
  unsigned long tube_two_hits;
  unsigned long tube_three_hits;
  unsigned long tube_four_hits;

  File file;

void setup() {
  // interrupt pins setup:
  const short tube_one_interrupt = 0;
  const short tube_two_interrupt = 1;
  const short tube_three_interrupt = 2;
  const short tube_four_interrupt = 3;

  pinMode(tube_one_interrupt, INPUT);
  pinMode(tube_two_interrupt, INPUT);
  pinMode(tube_three_interrupt, INPUT);
  pinMode(tube_four_interrupt, INPUT);

  attachInterrupt(digitalPinToInterrupt(tube_one_interrupt), hit_one, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_two_interrupt), hit_two, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_three_interrupt), hit_three, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_four_interrupt), hit_four, HIGH);

  // counter set up:
  timestamp = 0;
  tube_one_hits = 0;
  tube_two_hits = 0;
  tube_three_hits = 0;
  tube_four_hits = 0;

  while (!SD.begin()) {} // force the Arduino to open the SD card.
  Serial.println("SD Card Opened!");
 // use the cs select pin if necessary

  /*
   * SD card attached to SPI bus as follows:
   ** MOSI - pin 11
   ** MISO - pin 12
   ** CLK - pin 13
   ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)
   * cspin (optional): the pin connected to the chip select line of the SD card; defaults to the hardware SS line of the SPI bus 
   */
}

void loop() {
  delay(10);
  timestamp++; // timestamp is counting hundredths of a second
  // Arduino will wait for interrupt events to call functions below,
  // no other real business is performed.
}

void PrintToSerial(int tube, unsigned long hits, unsigned long timestamp)
{
  // "[Tube 0x]   Hits: xx    Time: xx.xx"
  Serial.print("[Tube 0");
  Serial.print(tube);
  Serial.print("]\tHits: ");
  
  switch(tube)
  {
    case 1: Serial.print(tube_one_hits);
      break;
    case 2: Serial.print(tube_two_hits);
      break;
    case 3: Serial.print(tube_three_hits);
      break;
    case 4: Serial.print(tube_four_hits);
  }
  
  Serial.println("\tTime: " + (timestamp / 100));
}

void PrintToFile(int tube, unsigned long hits, unsigned long timestamp)
{
  // "tube0x.txt - Hits: xxx   Time: xx.xx"
  
  File file;
    switch(tube)
  {
    case 1: file = SD.open("tube01.txt", FILE_WRITE);
      break;
    case 2: file = SD.open("tube02.txt", FILE_WRITE);
      break;
    case 3: file = SD.open("tube03.txt", FILE_WRITE);
      break;
    case 4: file = SD.open("tube04.txt", FILE_WRITE);
  }

  file.print("Hits: ");
  file.print(hits);
  file.print("\tTime: ");
  file.println(timestamp);
  file.close();
}

void hit_one()
{
  //tube_one_hits += 1;
  PrintToSerial(1, ++tube_one_hits, (timestamp / 100));
  PrintToFile(1, tube_one_hits, (timestamp / 100));
}

void hit_two()
{
  //tube_two_hits += 1;
  PrintToSerial(2, ++tube_two_hits, (timestamp / 100));
  PrintToFile(2, tube_two_hits, (timestamp / 100));
}

void hit_three()
{
  //tube_three_hits += 1;
  PrintToSerial(3, ++tube_three_hits, (timestamp / 100));
  PrintToFile(3, tube_three_hits, (timestamp / 100));
}

void hit_four()
{
  //tube_four_hits += 1;
  PrintToSerial(4, ++tube_four_hits, (timestamp / 100));
  PrintToFile(4, tube_four_hits, (timestamp / 100));
}
