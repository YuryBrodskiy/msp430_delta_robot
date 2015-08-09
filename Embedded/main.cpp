#include <msp430g2553.h>
#include "new.h"
#include "Energia.h"


#ifndef TIMERA0_VECTOR
#define TIMERA0_VECTOR TIMER0_A0_VECTOR
#endif /* TIMER0_A0_VECTOR */


class  IStepable
{
public:
	virtual ~IStepable() {};
	virtual void step(int usec) = 0;
};

class Servo : public IStepable
{
public:
  Servo(int pin, int min_usec, int max_usec)
  : isActive(false)
  , m_pin(pin)
  , m_min_usec(min_usec)
  , m_max_usec(max_usec)
  , m_set_usec(0)
  {

  }

  ~Servo()
  {

  }
  bool isActive;
  //! Write pulse width in rad
  void writeAngle(float rad)
  {
	  this->writeTime(map(rad, 0, 180, m_min_usec,  m_max_usec));
  }
  void writeTime(int usec) 				//! Write pulse width in microseconds
  {
	  m_set_usec=usec;
  }
  float readAngle()                        //! returns current pulse width as an angle between 0 and 180 degrees
  {
	  return  map( this->readMicroseconds()+1, m_min_usec, m_max_usec, 0, 180);
  }
  int readMicroseconds()            // returns current pulse width in microseconds for this servo (was read_us() in first release)
  {
	  return m_set_usec;
  }
  virtual void step(int usec)
  {
	  if (this->isActive)
	  {
		  m_actual_usec +=usec;
		  m_actual_usec = m_actual_usec % m_refresh_interval;
		  if(m_actual_usec <= m_set_usec)
		  {
			 digitalWrite(this->m_pin, HIGH);
		  }
		  else
		  {
			  digitalWrite(this->m_pin, LOW);
		  }
	  }
	  else
	  {
		  m_actual_usec = 0;
	  }
  }
private:
   uint8_t m_pin;                 // index into the channel data for this servo
   int8_t  m_min_usec;                         // minimum is this value times 4 added to MIN_PULSE_WIDTH
   int8_t  m_max_usec;                         // maximum is this value times 4 added to MAX_PULSE_WIDTH
   int8_t  m_set_usec;
   int8_t  m_actual_usec;
   static const int m_refresh_interval = 20000;  // typical frequency of servo pwm signal
};

//
//#define MIN_PULSE_WIDTH       544     // the shortest pulse sent to a servo [uS]
//#define MAX_PULSE_WIDTH      2400     // the longest pulse sent to a servo [uS]
//#define DEFAULT_PULSE_WIDTH  1500     // default pulse width when servo is attached
//#define REFRESH_INTERVAL    20000     // servos refresh period in microseconds
//
//#define MAX_SERVOS              8
//
//#define INVALID_SERVO         255     // flag indicating an invalid servo index
//
//typedef struct  {
//  uint8_t nbr        :6 ;             // a pin number from 0 to 63
//  uint8_t isActive   :1 ;             // true if this channel is enabled, pin not pulsed if false
//} ServoPin_t;
//
//typedef struct {
//  ServoPin_t Pin;
//  unsigned int ticks;
//} servo_t;
//
//
//
//#define F_TIMER (F_CPU/8L)
//#define usToTicks(_us)    (( clockCyclesPerMicrosecond()* _us) / 8)     // converts microseconds to timer ticks (assumes prescale of 8)
//#define ticksToUs(_ticks) (( (unsigned)_ticks * 8)/ clockCyclesPerMicrosecond() ) // converts from ticks back to microseconds
//
//#define TRIM_DURATION       2                               // compensation ticks to trim adjust for digitalWrite delays // 12 August 2009
//
//
//#define SERVO_MIN() (MIN_PULSE_WIDTH - this->min * 4)  // minimum value in uS for this servo
//#define SERVO_MAX() (MAX_PULSE_WIDTH - this->max * 4)  // maximum value in uS for this servo
//
//
///************ static functions and data structures common to all instances ***********************/
//
//
//static servo_t servos[MAX_SERVOS]; // static array of servo structures
//static unsigned int ServoCount = 0; // the total number of attached servos
//
//static volatile int counter = 0; // Servo counter; -1 before first servo starts being serviced
//static volatile unsigned int totalWait = 0; // Total amount waited so far in the current period; after all servos, wait for the rest of REFRESH_INTERVAL
//
//#ifndef TIMERA0_VECTOR
//#define TIMERA0_VECTOR TIMER0_A0_VECTOR
//#endif /* TIMER0_A0_VECTOR */
//
//// Timer A0 interrupt service routine
//static void
//Timer_A(void)
//{
//  static unsigned long wait;
//  if (counter >= 0) {
//    /* Turn pulse off. */
//    digitalWrite(servos[counter].Pin.nbr, LOW);
//  }
//
//  /* Service next servo, while skipping any inactive servo records. */
//  do {
//    counter++;
//  /* counter is nonnegative, so it is save to type cast to unsigned */
//  } while (!servos[counter].Pin.isActive && (unsigned)counter < ServoCount);
//
//  /* Counter range is 0-ServoCount, the last count is used to complete the REFRESH_INTERVAL
//   * counter is nonnegative, so it is save to type cast to unsigned */
//  if ((unsigned)counter < ServoCount) {
//    /* Turn pulse on for the next servo. */
//    digitalWrite(servos[counter].Pin.nbr, HIGH);
//    /* And hold! */
//    totalWait += servos[counter].ticks;
//    TA0CCR0 = servos[counter].ticks;
//  } else {
//    /* Wait for the remaining of REFRESH_INTERVAL. */
//    wait = usToTicks(REFRESH_INTERVAL) - totalWait;
//    totalWait = 0;
//    TA0CCR0 = (wait < 1000 ? 1000 : wait);
//    counter = -1;
//  }
//}
//
//// Timer A0 interrupt service routine
//__attribute__((interrupt(TIMERA0_VECTOR)))
//static void
//Timer_A_int(void)
//{
//  Timer_A();
//}
//
//static boolean isTimerActive(void)
//{
//  // returns true if any servo is active
//  for(int i = 0; i < MAX_SERVOS; i++)
//    if (servos[i].Pin.isActive == true)
//      return true;
//  return false;
//}
//
//static void enableTimer(void)
//{
//  counter = -1;
//  totalWait = 0;
//
//  Timer_A(); // enable first servo
//
//  TA0CCTL0 = CCIE;                             // CCR0 interrupt enabled
//  TA0CTL = TASSEL_2 + MC_1 + ID_3;           // prescale SMCLK/8, upmode
//}
//
//static void disableTimer(void)
//{
//  // disable interrupt
//  TA0CCTL0 = 0;
//  TA0CCR0 = 0;
//}
//
//
///****************** end of static functions ******************************/
//
//
//
//
//void Servo::write(int value)
//{
//  if(value < MIN_PULSE_WIDTH)
//  {  // treat values less than 544 as angles in degrees (valid values in microseconds are handled as microseconds)
//    if(value < 0) value = 0;
//    if(value > 180) value = 180;
//
//  }
//  this->writeMicroseconds(value);
//}
//
//void Servo::writeMicroseconds(int value)
//{
//  // calculate and store the values for the given channel
//  byte channel = this->servoIndex;
//  if( (channel < MAX_SERVOS) )   // ensure channel is valid
//  {
//    if( value < SERVO_MIN() )          // ensure pulse width is valid
//      value = SERVO_MIN();
//    else if( value > SERVO_MAX() )
//      value = SERVO_MAX();
//    value = value - TRIM_DURATION;
//    volatile int v = usToTicks(value);  // convert to ticks after compensating for interrupt overhead - 12 Aug 2009
//    servos[channel].ticks = v; // this is atomic on a 16bit uC, no need to disable Interrupts
//  }
//}
//
//int Servo::read() // return the value as degrees
//{
//  return  map( this->readMicroseconds()+1, SERVO_MIN(), SERVO_MAX(), 0, 180);
//}
//

Servo servo(5, 450, 2450);

int main(void)
{


	  pinMode(RED_LED, OUTPUT);
	  pinMode(GREEN_LED, OUTPUT);
	  servo.isActive=true;
	  servo.writeTime(1200);
	//  WDTCTL = WDT_ADLY_1000;			// Stop WDT
	//  IE1 |= WDTIE; // Enable WDT interrupt
delay(10);


	    // VLO is running at 12 kHz
	    TACCR0 = 240;//12000;    // the number of counts in the entire period
	    TACCR1 = 12;        // the number of counts the output signal is set on register 1 
        TACCR2 = 12;        // the number of counts the output signal is set on register 2

	    TACCTL1 |= OUTMOD_7;    // PWM output mode: 7 - PWM reset/set
        TACCTL2 |= OUTMOD_7;    // PWM output mode: 7 - PWM reset/set
	    
        // select P1.6 function as TA0.1
	    P1SEL |= BIT6;
	   // P1SEL2 &= BIT6;
	  BCSCTL1 |= DIVA_3;				// ACLK/8
	  BCSCTL3 |= XCAP_3;				//12.5pF cap- setting for 32.768Hz crystal
	  CCTL0 = CCIE;                                 // CCR0 interrupt enabled
	  TACTL = TASSEL_1 + MC_1 + ID_3;       // SMCLK/8, upmode
	  CCR0 = 10; //512/10// 100000;                         // 12.5 Hz
	 _BIS_SR(LPM3_bits + GIE);			// Enter LPM3 w/ interrupt




}


#pragma vector=TIMER0_A0_VECTOR
__interrupt void
Timer_A_int(void)
{
	servo.step(5);
}

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
