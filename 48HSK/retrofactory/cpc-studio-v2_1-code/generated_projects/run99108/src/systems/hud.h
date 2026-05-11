#ifndef _HUD_H_
#define _HUD_H_

#include <types.h>

void hud_init(void);
void hud_render(void);
void hud_update_score(u16 points);
void hud_update_health(u8 health);
void hud_update_lives(u8 lives);

#endif