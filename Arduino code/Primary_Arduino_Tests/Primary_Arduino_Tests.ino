// Basic tests to confirm Aruduino functionality

int x = 0; 

void setup() {
  // setup variables here
  Serial.begin(9600);
}

void loop() {
  // Delay a second and print time
  delay(1000);
  TimeToSerial();
}

void TimeToSerial()
{
  Serial.print("Second:");
  Serial.print("");
  Serial.print(x++);
}

