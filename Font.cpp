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

Glyph_t *_glyphs_ptr;
uint8_t _glyphs_offset=0;
uint8_t _glyphs_count=0;

void _draw_row(uint8_t row, int x, int y, uint8_t set) {
    int xx = x;
    //Serial.println(row);
    while(row) {
        uint8_t lsbset = row&0x1;
        LedSign::Set(xx,y, set?lsbset:!lsbset);
        row = row>>1;
        xx+=1;
    }
}

uint8_t Font::SetGlyphs(Glyph_t *glyphs, uint8_t offset, uint8_t count) {
    _glyphs_ptr = glyphs;
    _glyphs_offset = offset;
    _glyphs_count = count;
}

int8_t Font::Draw(uint8_t letter,int x, int y, uint8_t set, uint8_t width) {
    //Serial.print(x);
    //Serial.print(' ');
    //Serial.println(y);

    if (letter == ' ') return 0;
    if (letter > _glyphs_offset + _glyphs_count) return -1;
    if (letter < _glyphs_offset) return -1;

    Glyph_t *gptr = _glyphs_ptr+letter-_glyphs_offset;

    y += gptr->yoffset;
    for (int idx; idx < 8; ++idx) {
        _draw_row(gptr->rows[idx], x, y+idx, set);
    }
    
    if (width) return width;
    else return gptr->width;
}
