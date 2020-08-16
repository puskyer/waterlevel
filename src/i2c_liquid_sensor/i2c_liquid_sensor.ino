/***************************************************
* Liquid Level Sensor-XKC-Y25-T12V
* ****************************************************
* This example is to get liquid level

* @author jackli(Jack.li@dfrobot.com)
* @version  V1.0
* @date  2016-1-30

* GNU Lesser General Public License.
* See <http://www.gnu.org/licenses/> for details.
* All above must be included in any redistribution
* ****************************************************/
#include <Arduino.h>
#include <avr/wdt.h>
#include <Wire.h>

// I2C slave address for arduino
#define SLAVE_ADDRESS 0x08
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led0 = 13;

int liqSHin = 5;
byte Liquid_High_level=0;
int liqSLin = 6;
byte Liquid_Low_level=0;

byte data_send[2] = {0,0};
byte data_recived[2] = {0,0};
byte command_recived = 0;
byte data_recived_count = 0;



void setup() {

    Serial.begin(115200);  // start serial
    while(!Serial){} // Waiting for serial connection
    
    delay(1000);  
    Serial.println();
    Serial.println("Start I2C comm");
      // initialize the Liquid Sensor pin as an input.
    pinMode(liqSin,INPUT);
    Serial.print("Liquid Sensor pin is ");
    Serial.println(liqSin);
    
      // initialize the led pin as an output.
    pinMode(led0, OUTPUT);  
    Serial.println("Led is enabled ");
    
    // Wire communication begin
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);


}

void loop() {


  Liquid_High_level=digitalRead(liqSHin);
  Liquid_Low_level=digitalRead(liqSLin);


  if ( Liquid_High_level == 0 ) {

  
  data_send[0] = Liquid_level;

    switch (data_recived[0]) {
        case 1:
        //do something when data_recived is 1
          Serial.print("data_recived_count  ");
          Serial.println(data_recived_count, HEX);
          Serial.print("Recived command ");
          Serial.println(data_recived[0], HEX);
          digitalWrite(led0, HIGH);   // turn the LED on (HIGH is the voltage level)
          Serial.println("Led turned on!");
          Serial.print("Liquid level is ");
          Serial.println(data_send[0],HEX);
          data_recived[0] = 0;
          break;
        case 2:
        //do something when data_recived is 2
          Serial.print("Recived command ");
          Serial.print(data_recived[0], HEX);
          digitalWrite(led0, LOW);    // turn the LED off by making the voltage LOW
          Serial.println(" Led turned off!");
          Serial.print("Liquid level is ");
          Serial.println(data_send[0],DEC);
          data_recived[0] = 0;
          break;
        default:
          // if nothing else matches, do the default
 //         Serial.print("Liquid level is ");
 //         Serial.println(data_send[1],DEC);
          // default is optional
          break;
      }

  delay(500);

}

void receiveData(int bytecount){
  for (int i = 0; i < bytecount; i++) {
    data_recived[i] = Wire.read();
  }
  // the reset 
  if ( data_recived[0] == 0xde && data_recived[1] == 0xad) {
     _SoftwareReset();
     Serial.println("Reset!");
     } else {
     data_recived_count = bytecount;      
     }
}

void sendData(){
//    if (Wire.available() > 0){
      for (int i=0; i < data_recived_count; i++){
        Serial.print("data_send ");
        Serial.println(data_send[i],HEX);
        Wire.write(data_send[i]);
      }
      data_recived_count = 1;
//    }
}

// Restarts program from beginning but does not reset the peripherals and registers
void _SoftwareReset() {
  wdt_enable(WDTO_15MS);
} 


// function that executes whenever data is received from master
void receiveEvent(int arg) {
  int addr;
  int data;
  data_recived_count = 2;
  // receive bytes from i2c bus
  while (Wire.available() > 0) {
    // read the register address being written to
    addr  = Wire.read();

    // handle received commands and data
    if (Wire.available() > 0) {
      data = Wire.read();

      // the reset 
      if (addr == 0xde && data == 0xad) {
        _SoftwareReset();
        Serial.println("Reset!");
      } else {
          data_recived[0] = addr;
          data_recived[1] = data;
        }
    }
  }
}
