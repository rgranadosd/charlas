#include <cpctelera.h>

void main(void) {
   cpct_disableFirmware();
   cpct_setVideoMode(0);
   cpct_setBorder(0x4C);  // hw colour: bright red
   cpct_clearScreen(0x55); // mode 0: nibble pattern -> visible solid colour

   while (1);
}
