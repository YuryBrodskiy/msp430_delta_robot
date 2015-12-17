#include <msp430g2553.h>
#include "new.h"
#include "Energia.h"
#include "HardwareSerial.h"
#include "PWMServo.h"






int main(void)
{
  //! setup the clock Arduino based
  init();
  //! setup communication
  Serial.begin(9600);
  ServoMessage messageSource(&Serial);
  Serial.println("Start of setup");
  
  //! Assign pins
  delta::PWMServo servo1(P2_2);
  delta::PWMServo servo2(P2_5);
  delta::PWMServo servo3(P2_6);
  pinMode(RED_LED, OUTPUT);     // Indicate start of setup
  pinMode(GREEN_LED, OUTPUT);   // Indicate start of setup
  //! Setup power mode  
//?  LPM0_EXIT; //Do not care for power consumption servos aremuch more power hungry 
  
  Serial.println("End of setup");
  //!Start main loop
  while(1)
  {
    //Blocking Poll for message
    messageSource.read(); 
    //write to servos
    servo1.writeTime(messageSource.num[0]);
    servo2.writeTime(messageSource.num[1]);
    servo3.writeTime(messageSource.num[2]);
     //indicate loop complete
    digitalWrite(RED_LED, !digitalRead(RED_LED));
  }

  // can not finish
  digitalWrite(GREEN_LED, !digitalRead(GREEN_LED)); //indicate FAILURE
}

