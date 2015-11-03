/*
 * PWMServo.cpp
 *
 *  Created on: Aug 30, 2015
 *      Author: yury
 */

#include "PWMServo.h"
#include <msp430g2553.h>

namespace delta
{
  bool PWMServo::m_initialized = false;

  PWMServo::PWMServo(int pin)
  : m_pin(pin)
  , m_set_usec(0)
  {
    this->initialize();
  }

  PWMServo::~PWMServo()
  {
      
  }
  void PWMServo::writeTime(int usec) 				//! Write pulse width in microseconds
  {
    if (m_set_usec!=usec)
    {
      analogWrite(m_pin,m_set_usec);
    }
    m_set_usec=usec;
  }
  int PWMServo::readMicroseconds()            //! returns current pulse width in microseconds for this servo (was read_us() in first release)
  {
    return m_set_usec;
  }
  void PWMServo::initialize()
  {
    if(!m_initialized)
      {
        analogFrequency(PWMServo::m_freq); //
        analogResolution(PWMServo::m_res);
        m_initialized=true;
      }
  }
}
