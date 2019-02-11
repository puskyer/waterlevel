const int analogInPin = A0; 
int sensorValue = 0;

void setup() {
 Serial.begin(9600); 
}
 
void loop() {
 int sensorValue = analogRead(analogInPin); 
 // Serial.print("WaterLevel = " ); 
 Serial.println(sensorValue*100/1024); 
 //Serial.println("");
 delay(1000); 
}
