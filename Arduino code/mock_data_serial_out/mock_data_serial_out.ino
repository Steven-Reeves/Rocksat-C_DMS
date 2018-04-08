/*
 * By Steven Reeves
 * 
 * Serial data to RockSat-C DMS
 */

int x = 0; 

void setup() {
  Serial.begin(9600);

}

void loop() {
  // Edit [Mock 1] to identify each machine
  Serial.print("[Mock 1] Line: ");
  Serial.println(x, DEC);
  x++;
  // Actual delay used in RTC_GYRO_ACCEL
  delay(100);
}
