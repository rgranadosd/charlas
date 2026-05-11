#ifndef _HUD_H_
#define _HUD_H_

#include <cpctelera.h>

void hud_init(void);
void hud_draw(void);
void hud_update_score(u16 score);
void hud_update_lives(u8 lives);
void hud_update_health(u8 health);

#endif