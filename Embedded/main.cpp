#include <msp430g2553.h>

int main(void)
{
    WDTCTL = WDTPW + WDTHOLD;    // Stop watchdog timer

    BCSCTL1 &= ~XTS;        // LFXTCLK 0:Low Freq.
    BCSCTL3 |= LFXT1S_2;    // Mode 2 for LFXT1 : VLO

    TA0CTL = TASSEL_1    // Timer A clock source select: 1 - ACLK
            + MC_1;        // Timer A mode control: 1 - Up to CCR0

    // VLO is running at 12 kHz
    TA0CCR0 = 12000;    // the number of counts in the entire period
    TA0CCR1 = 6000;        // the number of counts the output signal is set

    TA0CCTL1 |= OUTMOD_7;    // PWM output mode: 7 - PWM reset/set

    // select P1.6 function as TA0.1
    P1SEL |= BIT6;
    P1SEL2 &= BIT6;

    P1DIR |= BIT6;    // P1.6 to output

    while(1)
    {
        LPM3;    // Enter Low Power Mode 3 - CPU Off, MCLK Off, SMCLK Off, DCO Off, ACLK On
    }
}