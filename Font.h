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

#ifndef Font_h
#define Font_h

#include <inttypes.h>

typedef uint8_t Glyph[3];

namespace Font
{

extern uint8_t SetGlyphs(Glyph *glyphs, uint8_t offset, uint8_t count);
/**
 * Returns the width of the letter, -1 if unsuccessful, 0
 * if a space was requested.
 *
 * Note that even if the letter isn't drawn, e.g. out of range, the width
 * is returned none the less.
 */ 
extern int8_t Draw(uint8_t letter, int x, int y,uint8_t set=1);

}

#endif

