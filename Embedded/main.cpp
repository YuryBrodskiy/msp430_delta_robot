#include <msp430g2553.h>

int main(void)
{
	  // put your setup code here, to run once:
	   //  WDTCTL = WDTPW + WDTHOLD;    // Stop watchdog timer

	    BCSCTL1 &= ~XTS;        // LFXTCLK 0:Low Freq.
	    BCSCTL3 |= LFXT1S_2;    // Mode 2 for LFXT1 : VLO

	    TACTL = TASSEL_1    // Timer A clock source select: 1 - ACLK
	            + MC_1;        // Timer A mode control: 1 - Up to CCR0

	    // VLO is running at 12 kHz
	    TACCR0 = 240;//12000;    // the number of counts in the entire period
	    TACCR1 = 12;        // the number of counts the output signal is set

	    TACCTL1 |= OUTMOD_7;    // PWM output mode: 7 - PWM reset/set

	    // select P1.6 function as TA0.1
	    P1SEL |= BIT6;
	   // P1SEL2 &= BIT6;

	    P1DIR |= BIT6;    // P1.6 to output

	    int i = 0;
	   while (1)
	   {
 
	    i=i+1;
	    i= i % 24;
	    TACCR1 = i;

	   }
}
