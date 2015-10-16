#include <msp430g2553.h>
#include "new.h"
#include "Energia.h"
#include "HardwareSerial.h"
#include "PWMServo.h"



const float pi = 3.1416;
const uint16_t low_val = 450;
const uint16_t high_val = 2450;
volatile int val = low_val;

typedef float Scalar;
const char lastWhitespace = 32;

void skipWhites(Stream* const input)
{
  while(input->available()>0 && ((char)input->timedPeek())<=lastWhitespace)
  {
    input->read();
  }

}

class  ServoMessage
{
public:
  ServoMessage(Stream* const input)
  {
    mInput = input;
    mInput->setTimeout(100);
    num[0]=0;
    num[1]=0;
    num[2]=0;
  }
  void read()
  {
    Scalar val[3];
    bool goodMessage = true;
    if(mInput->find("["))
    {
        val[0]=mInput->parseFloat();
        //goodMessage&=mInput->find(",");

        val[1]=mInput->parseFloat();
        //goodMessage&=mInput->find(",");

        val[2]=mInput->parseFloat();

        //goodMessage&=mInput->find("]");
        if(goodMessage)
          {
            num[0]=val[0];
            num[1]=val[1];
            num[2]=val[2];
          }
    }
  }
  void println()
  {
    mInput->print("[");mInput->print(num[0]);
    mInput->print(",");mInput->print(num[1]);
    mInput->print(",");mInput->print(num[2]);
    mInput->print("]");mInput->print("\n");
    mInput->clearWriteError();
  }
  Scalar num[3];
private:
  Stream* mInput;
};


int main(void)
{
  init(); // setup the clock
  Serial.begin(9600);
  Serial.println("Start of setup");
  delta::PWMServo servo1(P2_2, 0, pi, low_val, high_val);
  delta::PWMServo servo2(P2_5, 0, pi, low_val, high_val);
  delta::PWMServo servo3(P2_6, 0, pi, low_val, high_val);
  ServoMessage messageSource(&Serial);
  pinMode(RED_LED, OUTPUT); // Indicate start of setup
  pinMode(GREEN_LED, OUTPUT); // Indicate start of setup

  volatile int val_old = 0;
  _BIS_SR(LPM0_bits);
  Serial.println("End of setup");

  while(1){
      if(millis() % 20 == 0 )
        {

          messageSource.read();
          servo1.writeAngle(messageSource.num[0]);
          servo2.writeAngle(messageSource.num[1]);
          servo3.writeAngle(messageSource.num[2]);
          messageSource.println();
         digitalWrite(RED_LED, !digitalRead(RED_LED));
       }



  }; // can not finish
}
int divider = 0;

//#ifndef TIMERA0_VECTOR
//#define TIMERA0_VECTOR TIMER0_A0_VECTOR
//#endif /* TIMER0_A0_VECTOR */

//#pragma vector=WDT_VECTOR
//__interrupt  void
//Timer_A_int(void)
//{
//  if(divider == 20)
//    {
//      ///digitalWrite(GREEN_LED, !digitalRead(GREEN_LED));
//      val = max((val+50) % high_val,low_val);
//      divider =0;
//    }
//  divider++;
//}

// build in PWM below
//int main(void)
//{
//	  // put your setup code here, to run once:
//	   //  WDTCTL = WDTPW + WDTHOLD;    // Stop watchdog timer
//
//	    BCSCTL1 &= ~XTS;        // LFXTCLK 0:Low Freq.
//	    BCSCTL3 |= LFXT1S_2;    // Mode 2 for LFXT1 : VLO
//
//	    TACTL = TASSEL_1    // Timer A clock source select: 1 - ACLK
//	            + MC_1;        // Timer A mode control: 1 - Up to CCR0
//
//	    // VLO is running at 12 kHz
//	    TACCR0 = 240;//12000;    // the number of counts in the entire period
//	    TACCR1 = 12;        // the number of counts the output signal is set
//
//	    TACCTL1 |= OUTMOD_7;    // PWM output mode: 7 - PWM reset/set
//
//	    // select P1.6 function as TA0.1
//	    P1SEL |= BIT6;
//	   // P1SEL2 &= BIT6;
//
//	    P1DIR |= BIT6;    // P1.6 to output
//
//	    int i = 0;
//	   while (1)
//	   {
//
//	    i=i+1;
//	    i= i % 24;
//	    TACCR1 = i;
//
//	   }
//}
