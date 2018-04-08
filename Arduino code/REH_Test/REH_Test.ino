/*
 * By Caleb Ives
 * Modified by Steven Reeves
 * 
 * Based on examples provided by 
 * Adafruit.com Written by Kevin Towns
 * 
 * REH_Test.ino
 * Stubbed out code for initial testing.
 */
 
#include <Wire.h> 
// Commented out libraries
//#include <Adafruit_L3GD20.h>
//#include "RTClib.h"

// Comment this next line to use SPI
#define USE_I2C

//Adafruit_L3GD20 gyro;
//RTC_DS1307 rtc;

//Accelerometer
const int xInput = A0;
const int yInput = A1;
const int zInput = A2;
const int sampleSize = 1;


void setup() {
  analogReference(EXTERNAL);
  Serial.begin(57600);
  // Commented out begin checks
  /*
    if (!gyro.begin(gyro.L3DS20_RANGE_250DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_500DPS))
  //if (!gyro.begin(gyro.L3DS20_RANGE_2000DPS))
  {
    Serial.println("Unable to initialize Gyro!");
    while (1);
  }
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
  

  if (! rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date 
    // & time this sketch was compiled
    // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit
    // date & time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  } 
  */
}

void loop() {
  int xRaw = ReadAxis(xInput);
  int yRaw = ReadAxis(yInput);
  int zRaw = ReadAxis(zInput);
//  gyro.read();
//  DateTime now = rtc.now();

  //RTC output
   char dateBuffer[12];

  Serial.print("\t");
   // Static date
   // sprintf(dateBuffer,"%02u-%02u-%04u ",now.month(),now.day(),now.year());
   sprintf(dateBuffer,"%02u-%02u-%04u ",4,8,2018);
   Serial.print(dateBuffer);
   // Static time
   // sprintf(dateBuffer,"%02u:%02u:%02u ",now.hour(),now.minute(),now.second());
   sprintf(dateBuffer,"%02u:%02u:%02u ",13,49,15);
   Serial.print(dateBuffer);

  //Gyro output
  Serial.print("\t");
  Serial.print("| Gyro-> X: "); 
  Serial.print("\t");
  // Static x data
  //Serial.print((int)gyro.data.x);   
  Serial.print(42);  
  Serial.print("\t");
  Serial.print("Y: "); 
  Serial.print("\t");
  // Static y data
  //Serial.print((int)gyro.data.y);
  Serial.print(1900);   
  Serial.print("\t");
  Serial.print("Z: "); 
  Serial.print("\t");
  // Static y data
  //Serial.print((int)gyro.data.z);
  Serial.print(2000); 

  //Acceleromter Output
  Serial.print("\t");
  Serial.print("| Accel-> X:");
  Serial.print("\t");
  Serial.print(xRaw);
  Serial.print("\t");
  Serial.print("Y:");
  Serial.print("\t");
  Serial.print(yRaw);
  Serial.print("\t");
  Serial.print("Z:");
  Serial.print("\t");
  Serial.println(zRaw);
  delay(100);

}

// Read "sampleSize" samples and report 
//the average accelerometer reading
//
int ReadAxis(int axisPin)
{
  long reading = 0;
  analogRead(axisPin);
  delay(1);
  for (int i = 0; i < sampleSize; i++)
  {
    reading += analogRead(axisPin);
  }
  return reading/sampleSize;
}
