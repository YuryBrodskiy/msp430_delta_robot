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

  template <typename T1,typename T2>
  T2 map(T1 x, T1 in_min, T1 in_max, T2 out_min, T2 out_max)
  {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  }

  // servo 1 has to be on P1.2(UART), P1.6(GREEN_LED), P2.6 (XIN) uses TA0CCR0 TA0CCR1
  // servo 2 has to be on P2.1 or P2.2 uses TA1CCR0 TA1CCR1
  // servo 3 has to be on P2.4 or P2.5 uses TA1CCR0 TA1CCR2

  class PWMServo
  {
  public:
    PWMServo(int pin, float min_rad, float max_rad, int min_usec, int max_usec);
    ~PWMServo();
    void writeAngle(float rad);
    void writeTime(int usec); 				//! Write pulse width in microseconds
    float readAngle();                        //! returns current pulse width as an angle between 0 and 180 degrees
    int readMicroseconds();           // returns current pulse width in microseconds for this servo (was read_us() in first release)

  private:
    uint8_t m_pin;                 //! index into the channel data for this servo
    int  m_min_usec;            //! minimum duty cycle
    int  m_max_usec;            //! maximum duty cycle
    int  m_set_usec;			   //! current duty cycle
    float   m_min_rad;             //! minimum angle
    float   m_max_rad;             //! maximum angle
    float   m_set_rad;			   //! current angle
    bool    m_clocked;

  private: // fly weight
    static const uint32_t m_freq = 50;    //! Normal frequency of the Servos[Hz]
    static const uint16_t m_res =  20000; //! Maximum possible resolution for MSP430g2553 [% of full cycle]
    static bool m_initialized;
    static void initialize();
  };
}
#endif /* PWMSERVO_H_ */
