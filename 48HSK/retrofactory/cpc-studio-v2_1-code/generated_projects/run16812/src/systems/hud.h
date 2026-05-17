#ifndef SYSTEMS_HUD_H
#define SYSTEMS_HUD_H

#include <cpctelera.h>

void hudinit(void);
void hudupdate(u8 lives, u16 score, u8 time, u8 weapon);
void hudrender(void);

#endif
