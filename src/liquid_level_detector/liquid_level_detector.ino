const int analogInPin = A0; 
long sensorValue = 0;

void setup() {
 Serial.begin(9600); 
}
 
void loop() {
 long sensorValue = analogRead(analogInPin); 
 // Serial.print("WaterLevel = " ); 
 Serial.println((sensorValue*100)/1024); 
 // Serial.println((sensorValue/1024)*100);
 // Serial.println(sensorValue);  
 //Serial.println("");
 delay(1000); 
}
