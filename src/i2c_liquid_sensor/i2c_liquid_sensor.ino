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
/*
 *  modified to work with Onion Omega R1 and Adruino Dock v1
 */

#include <Arduino.h>
#include <avr/wdt.h>
#include <Wire.h>
#include <OnionLibrary.h>

// I2C slave address for arduino
#define SLAVE_ADDRESS 0x08

Onion* onionSetup;

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led0 = 13;

#define Liquid_level_high 0x1    // this is the sensor on state
#define Liquid_level_low 0x0     // this is the sensor off state

int liqSHpin = 5;               // pin for high side sensor
byte Liquid_High_level=0;       // variable that will change from 0 to 1 for high side

int liqSLpin = 6;               // pin for low side sensor
byte Liquid_Low_level=0;        // variable that will change from 0 to 1 for low side

byte data_send[2] = {0,0};      // I2C - holds the sensor state high byte is the high level state, low byte is the low level state
byte data_received[2] = {0,0};   // I2C - high byte hold the request to send or both bytes 0xde 0xad to reset code.
byte data_received_count = 0;    // number of I2C bytes received

void receiveData(int);          // define receive data function
void sendData();                // define send data function

void setup() {

    onionSetup = new Onion;      // so that we can program the arduino dock with out pushing the reset
    
    Serial.begin(115200);        // start serial
    while(!Serial){}             // Waiting for serial connection

        // Wire communication begin
    Wire.begin(SLAVE_ADDRESS);
    
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    
    delay(500);
    
    Serial.println("Start I2C communication ready");
      // initialize the Liquid Sensor pins as an input.
    pinMode(liqSHpin,INPUT);
    Serial.print("Liquid Sensor High pin is ");
    Serial.println(liqSHpin);
    pinMode(liqSHpin,INPUT);
    Serial.print("Liquid Sensor Low pin is ");
    Serial.println(liqSLpin);
    
      // initialize the led pin as an output.
    pinMode(led0, OUTPUT);  
    Serial.println("Led is enabled ");
    
}

void loop() {


  Liquid_High_level=digitalRead(liqSHpin);
  Liquid_Low_level=digitalRead(liqSLpin);

// prepare to send status to Onion Omega
  data_send[0] = Liquid_High_level;
  data_send[1] = Liquid_Low_level;


  if ( Liquid_Low_level = 0 ) {
    // turnoff pump 
    } else if ( (Liquid_Low_level = 1) && (Liquid_High_level = 0) ) {
    // monitor if pump is on then lets wait until we need to turn it off liquid low level false (0)
    // if pump is off then lets monitor until the liquid high level is true (1)  
    } else if ( (Liquid_Low_level = 1) && (Liquid_High_level = 1) ) {
    // turn on pump lets start emptying the container
    }

    switch (data_received[0]) {
        case 1:
        //do something when data_recived is 1
//          Serial.print("data_recived_count  ");
//          Serial.println(data_received_count, HEX);
          Serial.print("Received command ");
          Serial.println(data_received[0], HEX);
          digitalWrite(led0, HIGH);   // turn the LED on (HIGH is the voltage level)
          Serial.println("Led turned on!");
          Serial.print("Liquid High level state is ");
          Serial.println(data_send[0],HEX);
          Serial.print("Liquid Low level state is ");
          Serial.println(data_send[1],HEX);          
          data_received[0] = 0;
          break;
        case 2:
        //do something when data_recived is 2
          Serial.print("Received command ");
          Serial.print(data_received[0], HEX);
          digitalWrite(led0, LOW);    // turn the LED off by making the voltage LOW
          Serial.println(" Led turned off!");
          Serial.print("Liquid High level state is ");
          Serial.println(data_send[0],HEX);
          Serial.print("Liquid Low level state is ");
          Serial.println(data_send[1],HEX);
          data_received[0] = 0;
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
    data_received[i] = Wire.read();
  }
  // the reset 
  if ( data_received[0] == 0xde && data_received[1] == 0xad) {
     _SoftwareReset();
     Serial.println("Received Reset request!");
     } else {
     data_received_count = bytecount;      
     }
}

void sendData(){
      for (int i=0; i < sizeof(data_send); i++){
        Serial.print("data_send ");
        Serial.println(data_send[i],HEX);
      }
        Wire.write(data_send, sizeof(data_send));
}

// Restarts program from beginning but does not reset the peripherals and registers
void _SoftwareReset() {
  wdt_enable(WDTO_15MS);
} 


// function that executes whenever data is received from master
void receiveEvent(int arg) {
  int addr;
  int data;
  data_received_count = 2;
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
          data_received[0] = addr;
          data_received[1] = data;
        }
    }
  }
}
