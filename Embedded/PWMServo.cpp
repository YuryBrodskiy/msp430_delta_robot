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

  PWMServo::PWMServo(int pin, float min_rad, float max_rad, int min_usec, int max_usec)
  : m_pin(pin)
  , m_min_usec(min_usec)
  , m_max_usec(max_usec)
  , m_set_usec(0)
  , m_min_rad(min_rad)
  , m_max_rad(max_rad)
  , m_set_rad(0)
  {
    this->initialize();
  }

  PWMServo::~PWMServo()
  {
    writeTime(0);
  }
  void PWMServo::writeAngle(float rad)
  {
    m_set_rad = rad;
    this->writeTime(delta::map(m_set_rad, m_min_rad, m_max_rad, m_min_usec,  m_max_usec));
  }
  void PWMServo::writeTime(int usec) 				//! Write pulse width in microseconds
  {
    if (m_set_usec!=usec)
      analogWrite(m_pin,m_set_usec);
    m_set_usec=usec;
  }
  float PWMServo::readAngle()                        //! returns current pulse width as an angle between 0 and 180 degrees
  {
    return  delta::map( m_set_usec, m_min_usec, m_max_usec, m_min_rad, m_max_rad);
  }
  int PWMServo::readMicroseconds()            // returns current pulse width in microseconds for this servo (was read_us() in first release)
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
