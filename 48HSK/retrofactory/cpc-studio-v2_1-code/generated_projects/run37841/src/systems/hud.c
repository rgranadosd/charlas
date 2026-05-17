#include "systems/hud.h"

static u8  currenthealth;
static u16 currentscore;
static u8  currenttime;
static u8  currentlives;
static u8  currentweapon;

static const u8 hudhealth[] = {
    cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6),
};

static const u8 hudlives[] = {
    cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(4, 4),
    cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4), cpct_px2byteM0(4, 4),
};

static const u8 huddigit_0[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_1[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_2[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_3[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_4[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_5[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_6[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_7[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_8[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};
static const u8 huddigit_9[] = {
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6),
    cpct_px2byteM0(0, 0), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(6, 6), cpct_px2byteM0(0, 0),
};

/* GSINIT-safe digit lookup: a function avoids initialised pointer arrays
   (those require the INITIALIZER -> DATA copy that --no-std-crt0 skips). */
static const u8* hud_get_number_sprite(u8 digit) {
    switch (digit % 10) {
    case 0: return huddigit_0;
    case 1: return huddigit_1;
    case 2: return huddigit_2;
    case 3: return huddigit_3;
    case 4: return huddigit_4;
    case 5: return huddigit_5;
    case 6: return huddigit_6;
    case 7: return huddigit_7;
    case 8: return huddigit_8;
    default: return huddigit_9;
    }
}

static void hud_draw_digits(u16 value, u8 digits, u8 startx, u8 y) {
    u8 i;
    u8 digit;
    u16 divisor;
    u8* pvmem;

    divisor = 1;
    for (i = 1; i < digits; ++i) {
        divisor *= 10;
    }

    for (i = 0; i < digits; ++i) {
        digit = (u8)(value / divisor);
        value = (u16)(value % divisor);

        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, startx + (i * 8), y);
        cpct_drawSprite((u8*)hud_get_number_sprite(digit), pvmem, 8, 8);

        if (divisor > 1) {
            divisor /= 10;
        }
    }
}

void hudinit(void) {
    currenthealth = 3;
    currentscore  = 0;
    currenttime   = 90;
    currentlives  = 3;
    currentweapon = 0;
}

void hudupdate(u8 lives, u16 score, u8 time, u8 weapon) {
    currenthealth = lives;
    currentscore  = score;
    currenttime   = time;
    currentlives  = lives;
    currentweapon = weapon;
}

void hudrender(void) {
    u8 i;
    u8* pvmem;
    u16 scoretemp;
    u8 timetemp;

    for (i = 0; i < currenthealth; ++i) {
        pvmem = cpct_getScreenPtr(CPCT_VMEM_START, (i * 8), 2);
        cpct_drawSprite((u8*)hudhealth, pvmem, 8, 8);
    }

    scoretemp = currentscore;
    hud_draw_digits(scoretemp, 4, 24, 2);

    timetemp = currenttime;
    hud_draw_digits((u16)timetemp, 3, 56, 2);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 2, 180);
    cpct_drawSprite((u8*)hudlives, pvmem, 8, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 12, 180);
    cpct_drawSprite((u8*)hud_get_number_sprite(currentlives % 10), pvmem, 8, 8);

    pvmem = cpct_getScreenPtr(CPCT_VMEM_START, 70, 180);
    cpct_drawSprite((u8*)hud_get_number_sprite(currentweapon % 10), pvmem, 8, 8);
}
