/* Sweep
 by BARRAGAN <http://barraganstudio.com> 
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/ 

#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most boards

int numpos = 4;
int usecpos[4] = {1400, 1500, 1405, 1500};

//int numpos = 2;
//int usecpos[2] = {1492, 1500};


int lastpos = usecpos[0];

int stept = 1;
int waitt = 500;

void setup() 
{ 
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  for (int p = 0; p < numpos; p++) { 

    if (lastpos < usecpos[p]) {
      for (int us = lastpos; us < usecpos[p]; us++) { 
        myservo.writeMicroseconds(us);
        delay(stept);
      }
    } else {
      for (int us = lastpos; us > usecpos[p]; us--) { 
        myservo.writeMicroseconds(us);
        delay(stept);
      }      
    }
    lastpos = usecpos[p];
    delay(waitt);
  }
  
  
} 

