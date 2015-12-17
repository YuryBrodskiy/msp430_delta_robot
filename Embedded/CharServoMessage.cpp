/*
 * CharServoMessage.cpp
 *
 *  Created on: Dec 17, 2015
 *      Author: yury
 */

#include "CharServoMessage.h"

#include <msp430g2553.h>
#include "Energia.h"
#include "HardwareSerial.h"

CharServoMessage::CharServoMessage(Stream* const input)
{
  mInput = input;
  mInput->setTimeout(this->timeOut);
  num[0] = 0;
  num[1] = 0;
  num[2] = 0;
}
bool
CharServoMessage::read()
{
  waitForMessage(mInput);
  int buf[4];

  for (int i = 0; i < 4; i++)
    {
      int val1, val2;
      val1 = mInput->timedRead();
      val2 = mInput->timedRead();
      // mInput->print("[");mInput->print(val1); mInput->print(",");mInput->print(num[1]);mInput->print("]");
      buf[i] = decodeNumber(val1, val2);
      //   mInput->print(buf[i] );mInput->print("\n");
    }

  int checkSumComputed = buf[0] + buf[1] + buf[2];
  bool goodMessage = buf[3] == checkSumComputed;
  if (goodMessage)
    {
      num[0] = buf[0];
      num[1] = buf[1];
      num[2] = buf[2];
    }
  else
    {
      mInput->println("Message was corrupted");
    }
  return goodMessage;
}
void
CharServoMessage::println()
{
  mInput->print("[");
  mInput->print(num[0]);
  mInput->print(",");
  mInput->print(num[1]);
  mInput->print(",");
  mInput->print(num[2]);
  mInput->print("]");
  mInput->print("\n");
  mInput->flush();
  mInput->clearWriteError();
}

void
CharServoMessage::waitForMessage(Stream* const input)
{
  while (input->available() <= 0)
    {
    };
}
int
CharServoMessage::decodeNumber(int highBit, int lowBit)
{
  return (highBit << 8) + lowBit;
}

