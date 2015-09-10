#include <iostream>
#include <stdio.h>      // standard input / output functions
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions


//#define USB_SERIAL_PORT "/dev/tty.usbserial-0000103D" // (OSX Power Book)
//#define USB_SERIAL_PORT  "/dev/cu.usbserial-3B1" // (OSX Mac Book)
//#define USB_SERIAL_PORT "/dev/tty.usbserial-0000103D" // (Linux Ubuntu Mac Book)
//#define USB_SERIAL_PORT "/dev/tty.usbserial-0000103D"
#define USB_SERIAL_PORT "/dev/tty.uart-28FF467AF9D1272C" // (OSX Power Book)

int init_serial_input (char * port) {
  int fd = 0;
  struct termios options;

  fd = open(port, O_RDWR | O_NOCTTY | O_NDELAY);
  if (fd == -1)
    return fd;
    fcntl(fd, F_SETFL, 0);    // clear all flags on descriptor, enable direct I/O
    tcgetattr(fd, &options);   // read serial port options
    // enable receiver, set 8 bit data, ignore control lines
    options.c_cflag |= (CLOCAL | CREAD | CS8);
    // disable parity generation and 2 stop bits
    options.c_cflag &= ~(PARENB | CSTOPB);
    // set the new port options
    tcsetattr(fd, TCSANOW, &options);
    return fd;
}
int read_serial_int (int fd) {
  char ascii_int[8] = {0};
  char c = NULL;
  int i = 0;

  read(fd, &c, 1);
  //while (c != '\n')
  while (c != ' ')  {
    ascii_int[i++] = c;
    read(fd, &c, 1);
  }
  return atoi(ascii_int);
}

int main(int, char **)
{
	std::cout<<"Opening USB"<<std::endl;
	int	USB = open( USB_SERIAL_PORT, O_RDWR| O_NONBLOCK | O_NDELAY  );
	// serial is checked
	if (USB < 0)  {
		std::cout << "Couldn't open USB port" << std::endl;
	}
	else
	{
		std::cout<<"Success"<<std::endl;
	}

	struct termios tty;
	struct termios tty_old;
	memset (&tty, 0, sizeof tty);

	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 ) {
	   std::cout << "Error " << errno << " from tcgetattr: " << strerror(errno) << std::endl;
	}

	/* Save old tty parameters */
	tty_old = tty;

	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)B9600);
	cfsetispeed (&tty, (speed_t)B9600);

	/* Setting other Port Stuff */
	tty.c_cflag     &=  ~PARENB;            // Make 8n1
	tty.c_cflag     &=  ~CSTOPB;
	tty.c_cflag     &=  ~CSIZE;
	tty.c_cflag     |=  CS8;

	tty.c_cflag     &=  ~CRTSCTS;           // no flow control
	tty.c_cc[VMIN]   =  1;                  // read doesn't block
	tty.c_cc[VTIME]  =  5;                  // 0.5 seconds read timeout
	tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines

	/* Make raw */
	cfmakeraw(&tty);

	/* Flush Port, then applies attributes */
	tcflush( USB, TCIFLUSH );
	if ( tcsetattr ( USB, TCSANOW, &tty ) != 0) {
	   std::cout << "Error " << errno << " from tcsetattr" << std::endl;
	}

	char* cmd = "q\n";
	int n_written = write( USB, cmd, sizeof(cmd) -1);
	std::cout<<"Written "<<n_written<<std::endl;
	close(USB);
	return 0;
}
