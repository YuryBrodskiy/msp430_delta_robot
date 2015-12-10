#include <msp430g2553.h>
#include "new.h"
#include "Energia.h"
#include "HardwareSerial.h"
#include "PWMServo.h"



class ServoMessage
{
public:
  ServoMessage(Stream* const input)
  {
    mInput = input;
    mInput->setTimeout(this->timeOut);
    num[0]=0;
    num[1]=0;
    num[2]=0;
  }
  void read()
  {
    waitForMessage(mInput);
    int buf[3];
    buf[0] = mInput->read();
    buf[1] = mInput->read();
    buf[2] = mInput->read();
    int checkSumReceived = mInput->read();
    int checkSumComputed = buf[0]+buf[1]+buf[2];
    if(checkSumReceived==checkSumComputed)
    {
        num[0]=buf[0];
        num[1]=buf[1];
        num[2]=buf[2];
    }
    else
    {  
        mInput->println("Message was corrupted");
    }
  }
  void println()
  {
    mInput->print("[");mInput->print(num[0]);
    mInput->print(",");mInput->print(num[1]);
    mInput->print(",");mInput->print(num[2]);
    mInput->print("]");mInput->print("\n");
    mInput->flush();
    mInput->clearWriteError();
  }
  int num[3];
private:
  void waitForMessage(Stream* const input)
  {
	  while(input->available()<=0){};	
// timedPeek uses -1 as error code and only process chars but returns int (headbang)
	  while(input->available()>0 && ((int)input->timedPeek())!=beginMessage)
	  {
		  input->read();
	  }

  }
  Stream* mInput;
  static const int beginMessage =  -1;
  static const int timeOut = 1000; //![ms] wait for a next symbol
};


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

