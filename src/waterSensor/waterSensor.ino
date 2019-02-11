void setup () {

  // initialize serial communication at 9600 bits per second:

  Serial.begin (9600);

}

// the loop routine runs over and over again forever:

void loop() {

  // read the input on analog pin 0:

  int value = analogRead(A0);

  // print out the value you read:

  Serial.print (value);

  Serial.print("   ");

  delay(1000);     


if (value>660)

{

   Serial.println("HIGH");

}

else if ((value>600) && (value<=660))

{

Serial.println("AVERAGE");

}


else

{

  Serial.println("LOW");


}

}
