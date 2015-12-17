/*
 * StringServoMessage.h
 *
 *  Created on: Dec 17, 2015
 *      Author: yury
 */

#ifndef STRINGSERVOMESSAGE_H_
#define STRINGSERVOMESSAGE_H_

typedef float Scalar;
class Stream;

class  StringServoMessage
{
public:
  StringServoMessage(Stream* const input);
  bool read();
  void println();
  Scalar num[3];
private:
  Stream* mInput;
};


#endif /* STRINGSERVOMESSAGE_H_ */
