//char dataString[50] = {0};
//int a =0;
byte number = 0; 

void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {

  if (Serial.available()) {     // Check if message is recieved
      number = Serial.read();
      Serial.print("character recieved: ");
      Serial.println(number, DEC);
  }
  //a++;                          // a value increase every loop
  //sprintf(dataString,"%02X",a); // convert a value to hexa 
  //Serial.println(dataString);   // send the data
  //delay(1000);                  // give the loop some break
}
