/*
 * CharServoMessage.h
 *
 *  Created on: Dec 17, 2015
 *      Author: yury
 */

#ifndef CHARSERVOMESSAGE_H_
#define CHARSERVOMESSAGE_H_
class Stream;

class CharServoMessage
{
public:
  CharServoMessage(Stream* const input);
  bool read();
  void println();
  int num[3];
private:
  void waitForMessage(Stream* const input);
  int decodeNumber(int highBit, int lowBit);
  Stream* mInput;
  static const int timeOut = 1000; //![ms] wait for a next symbol
};

#endif /* CHARSERVOMESSAGE_H_ */
