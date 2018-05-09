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


  static unsigned long timestamp; // maximize counting range (0 - 4,294,967,295)
  static unsigned long tube_one_hits;
  static unsigned long tube_two_hits;
  static unsigned long tube_three_hits;
  static unsigned long tube_four_hits;

  File file;

void setup() {
  // interrupt pins setup:
  const int tube_one_interrupt = 0;
  const int tube_two_interrupt = 1;
  const int tube_three_interrupt = 2;
  const int tube_four_interrupt = 3;

  pinMode(tube_one_interrupt, INPUT);
  pinMode(tube_two_interrupt, INPUT);
  pinMode(tube_three_interrupt, INPUT);
  pinMode(tube_four_interrupt, INPUT);

  attachInterrupt(digitalPinToInterrupt(tube_one_interrupt), hit_one, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_two_interrupt), hit_two, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_three_interrupt), hit_three, HIGH);
  attachInterrupt(digitalPinToInterrupt(tube_four_interrupt), hit_four, HIGH);

  // counter set up:
  timestamp = 0; // maximize counting range (0 - 4,294,967,295)
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
  // put your main code here, to run repeatedly:
  timestamp++;
  delay(10); // count to one-hundredths of a second
}

void hit_one()
{
  tube_one_hits += 1;
  // print to serial that tube 1 received a hit of radiation.
  Serial.println("[Tube 01]\tHits: " + tube_one_hits);
  // write to SD card that tube 1 received a hit of radiation.
  file = SD.open("tube01.txt", FILE_WRITE);
  // if (file)
  // {
  //    file.writeln("[Tube 01]\tHits: %f\tTime: %d", tube_one_hits, (timestamp / 100));
  //    file.close();
  // }
  
}

void hit_two()
{
  tube_two_hits += 1;
  // print to serial that tube 2 received a hit of radiation.
  Serial.println("[Tube 02]\tHits: " + tube_two_hits);
  // write to SD card that tube 2 received a hit of radiation.
  file = SD.open("tube02.txt", FILE_WRITE);
  // if (file)
  // {
  //    file.writeln("[Tube 02]\tHits: %d\tTime: %f", tube_two_hits, (timestamp / 100));
  //    file.close();
  // }
}

void hit_three()
{
  tube_three_hits += 1;
  // print to serial that tube 3 received a hit of radiation.
  Serial.println("[Tube 03]\tHits: " + tube_three_hits);
  // write to SD card that tube 3 received a hit of radiation.
  file = SD.open("tube03.txt", FILE_WRITE);
  // if (file)
  // {
  //    file.writeln("[Tube 03]\tHits: %d\tTime: %f", tube_three_hits, (timestamp / 100));
  //    file.close();
  // }
}

void hit_four()
{
  tube_four_hits += 1;
  // print to serial that tube 4 received a hit of radiation.
  Serial.println("[Tube 04]\tHits: " + tube_four_hits);
  // write to SD card that tube 4 received a hit of radiation.
  file = SD.open("tube04.txt", FILE_WRITE);
  // if (file)
  // {
  //    file.writeln("[Tube 04]\tHits: %d\tTime: %f", tube_four_hits, (timestamp / 100));
  //    file.close();
  // }
}
