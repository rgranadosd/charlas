#ifndef AUDIO_H
#define AUDIO_H
#include <cpctelera.h>

#define SFX_WALL_HIT       0
#define SFX_PADDLE_HIT     1
#define SFX_BRICK_HIT      2
#define SFX_LIFE_LOST      3
#define SFX_GAME_OVER      4
#define SFX_LEVEL_COMPLETE 4

void audio_init(void);
void audio_update(void);
void audio_play_sfx(u8 sfx_id);

#endif /* AUDIO_H */
