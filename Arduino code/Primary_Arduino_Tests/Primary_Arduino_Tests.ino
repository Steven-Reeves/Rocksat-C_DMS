// Basic tests to confirm Aruduino functionality

int x = 0; 

byte number = 0;

void setup() {
  // setup variables here
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) 
  {
    number = Serial.read();
    Serial.print("character recieved: ");
    Serial.println(number, DEC);
  }  
  /*
  // Delay a second and print time
  delay(1000);
  TimeToSerial();
  */
}

void TimeToSerial()
{
  Serial.print("Second:");
  Serial.print(x++);
  Serial.println();
}


