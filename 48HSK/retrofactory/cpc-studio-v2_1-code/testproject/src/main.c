#include <cpctelera.h>

void main(void) {
    cpct_disableFirmware();
    cpct_setVideoMode(0);
    cpct_clearScreen(3);
    while (1) {}
}