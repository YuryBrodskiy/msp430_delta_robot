/*
 * PWMServo.h
 *
 *  Created on: Aug 30, 2015
 *      Author: yury
 */

#ifndef PWMSERVO_H_
#define PWMSERVO_H_
#include "Energia.h"
namespace delta
{
 
  // servo 1 has to be on P1.2(UART), P1.6(GREEN_LED), P2.6 (XIN) uses TA0CCR0 TA0CCR1
  // servo 2 has to be on P2.1 or P2.2 uses TA1CCR0 TA1CCR1
  // servo 3 has to be on P2.4 or P2.5 uses TA1CCR0 TA1CCR2

  class PWMServo
  {
  public:
    PWMServo(int pin);
    ~PWMServo();
    void writeTime(int usec); 				//! Write pulse width in microseconds
    int readMicroseconds();                 //! returns current pulse width in microseconds for this servo (was read_us() in first release)

  private:
    int  m_pin;                 //! index into the channel data for this servo
    int  m_set_usec;			   //! current duty cycle

  private: // fly weight
    static const uint32_t m_freq = 50;    //! Normal frequency of the Servos[Hz]
    static const uint16_t m_res =  20000; //! Maximum possible resolution for MSP430g2553 [% of full cycle]
    static bool m_initialized;
    static void initialize();
  };
}
#endif /* PWMSERVO_H_ */
