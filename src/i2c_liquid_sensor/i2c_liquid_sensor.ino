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
#include <Wire.h>

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led0 = 13;
int liqSpin = 5;
#define SLAVE_ADDRESS 0x08
byte data_send[2] = {0,0};
byte command_recived = 0;
byte data_recived[2] = {0,0};
byte data_recived_count = 0;

int Liquid_level=0;

void setup() {

    Wire.begin(); // Wire communication begin

    Serial.begin(115200);  // start serial
    while(!Serial){} // Waiting for serial connection
    
    delay(1000);  
    Serial.println();
    Serial.println("Start I2C comm");
      // initialize the Liquid Sensor pin as an input.
    pinMode(liqSpin,INPUT);
    Serial.print("Liquid Sensor pin is ");
    Serial.println(liqSpin);
    
      // initialize the led pin as an output.
    pinMode(led0, OUTPUT);  
    Serial.println("Led is enabled ");
    
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);


}

void loop() {


//  Liquid_level=digitalRead(5);
  Liquid_level = 5;
  data_send[1] = Liquid_level;
  
    switch (data_recived[0]) {
        case 1:
        //do something when data_recived is 1
          Serial.print("Recived command ");
          Serial.println(data_recived[0], DEC);
          Serial.print("data  ");
          Serial.println(data_recived[1], DEC);
          digitalWrite(led0, HIGH);   // turn the LED on (HIGH is the voltage level)
          Serial.println("Led turned on!");
          sendData();
          data_recived[0] = 0;
          break;
        case 2:
        //do something when data_recived is 2
          Serial.println(data_recived[0], DEC);
          Serial.print("data  ");
          Serial.println(data_recived[1], DEC);
          digitalWrite(led0, LOW);    // turn the LED off by making the voltage LOW
          Serial.print("Liquid level is ");
          Serial.println(data_send[1],DEC);
          data_recived[0] = 0;
          break;
        default:
          // if nothing else matches, do the default
          // default is optional
          break;
      }

  delay(500);

}

void receiveData(int bytecount)
{
  for (int i = 0; i < bytecount; i++) {
    data_recived_count = bytecount;
    data_recived[i] = Wire.read();
  }  
}

void sendData()
{
  for (int i=0; i < data_recived_count; i++) {
     Wire.write(data_send[i]);
  }
}
