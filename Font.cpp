/*
  Font drawing library

  Copyright 2009/2010 Benjamin Sonntag <benjamin@sonntag.fr> http://benjamin.sonntag.fr/
  
  History:
  	2010-01-01 - V0.0 Initial code at Berlin after 26C3

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330,
  Boston, MA 02111-1307, USA.
*/

#include "Font.h"
#include "Charliplexing.h"
#include <inttypes.h>

#include <Arduino.h>

Glyph *_glyphs_ptr;
uint8_t _glyphs_offset=0;
uint8_t _glyphs_count=0;

void _draw_row(uint8_t row, int x, int y, uint8_t set) {
    for (uint8_t idx = 0; idx < 4; ++idx) {
        int xx = x+idx;
        uint8_t lsbset = row&0x1;
        LedSign::Set(xx,y, set?lsbset:!lsbset);
        row = row>>1;
    }
}

uint8_t Font::SetGlyphs(Glyph *glyphs, uint8_t offset, uint8_t count) {
    _glyphs_ptr = glyphs;
    _glyphs_offset = offset;
    _glyphs_count = count;

    /*
    Serial.print(offset);
    Serial.print(" ");
    Serial.println(count);

    for (int idx = 0; idx < count; ++idx) {
        Serial.print("g[");
        Serial.print(idx);
        Serial.print("]=");
        Serial.print(" 0x");
        Serial.print(glyphs[idx][0], HEX);
        Serial.print(" 0x");
        Serial.print(glyphs[idx][1], HEX);
        Serial.print(" 0x");
        Serial.print(glyphs[idx][2], HEX);
        Serial.println("");
    }
    */
}

int8_t Font::Draw(uint8_t letter,int x, int y, uint8_t set) {
    if (letter == ' ') return 0;
    if (letter > _glyphs_offset + _glyphs_count) return -1;
    if (letter < _glyphs_offset) return -1;

    uint8_t *g = _glyphs_ptr[letter-_glyphs_offset];
    
    /*
    Serial.print("g:");
    Serial.print(" 0x");
    Serial.print(g[0]&0xFF, HEX);
    Serial.print(" 0x");
    Serial.print(g[1]&0xFF, HEX);
    Serial.print(" 0x");
    Serial.print(g[2]&0xFF, HEX);
    Serial.println("");
    */

    uint8_t b = g[0];
    uint8_t w = 1+((b&0xC0)>>6);
    uint8_t h = 1+((b&0x30)>>4);

    /*Serial.print(w);
    Serial.print(" x ");
    Serial.println(h);*/
    // first row
    b = b&0x0F;
    _draw_row(b, x, y, set);
    
    // second and third row
    b = (g[1]&0xF0)>>4;
    _draw_row(b, x, y+1, set);

    b = (g[1]&0x0F);
    _draw_row(b, x, y+2, set);
    
    // fourth row and fifth row
    b = (g[2]&0xF0)>>4;
    _draw_row(b, x, y+3, set);

    b = (g[2]&0x0F);
    _draw_row(b, x, y+4, set);

    return w;
}
