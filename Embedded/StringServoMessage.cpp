/*
 * StringServoMessage.cpp
 *
 *  Created on: Dec 17, 2015
 *      Author: yury
 */

#include "StringServoMessage.h"

#include <msp430g2553.h>
#include "Energia.h"
#include "HardwareSerial.h"

const char lastWhitespace = 32;

void
skipWhites(Stream* const input)
{
  while (input->available() > 0 && ((char) input->timedPeek())
      <= lastWhitespace)
    {
      input->read();
    }
}

StringServoMessage::StringServoMessage(Stream* const input)
{
  mInput = input;
  mInput->setTimeout(1000);
  num[0] = 0;
  num[1] = 0;
  num[2] = 0;
}

bool
StringServoMessage::read()
{
  Scalar val[3];
  bool goodMessage = true;
  if (mInput->find("["))
    {
      goodMessage = true;
      val[0] = mInput->parseFloat();
      // goodMessage&=mInput->find(",");

      val[1] = mInput->parseFloat();
      //goodMessage&=mInput->find(",");

      val[2] = mInput->parseFloat();

      //goodMessage&=mInput->find("]");
      if (goodMessage)
        {
          num[0] = val[0];
          num[1] = val[1];
          num[2] = val[2];
        }
    }
  return goodMessage;
}

void
StringServoMessage::println()
{
  mInput->print("[");
  mInput->print(num[0]);
  mInput->print(",");
  mInput->print(num[1]);
  mInput->print(",");
  mInput->print(num[2]);
  mInput->print("]");
  mInput->print("\n");
  mInput->clearWriteError();
}
