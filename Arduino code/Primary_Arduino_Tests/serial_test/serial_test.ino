char dataString[50];
int iter =0;
char a = 0;
byte number = 0;


void setup() {
Serial.begin(9600);              //Starting serial communication
}
  
void loop() {

  if (Serial.available()) {     // Check if message is recieved
      number = Serial.read();
      a = number;
      Serial.print("character recieved as DEC: ");
      Serial.println(number, DEC);
      Serial.print("character recieved as CHAR: ");
      Serial.println(a);
      dataString[iter++] = a;
      Serial.print("Full word so far: ");
      Serial.println(dataString);
  }
  //a++;                          // a value increase every loop
  //sprintf(dataString,"%02X",a); // convert a value to hexa 
  //Serial.println(dataString);   // send the data
  //delay(1000);                  // give the loop some break
}
