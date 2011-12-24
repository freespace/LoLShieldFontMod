#include <Charliplexing.h>
#include <Font.h>

#include "sifontv1.h"

char string[] = "@freespace #arduino";

void setup () {  
  Serial.begin(9600);
  delay(100);
  
  LedSign::Init(); 
  Font::SetGlyphs(Glyphs, Glyph_ASCII_Offset, Glyphs_Count);
}

int xoffset = 0;
int x,w;
void loop() {
  LedSign::Clear();
  x = 0;
  for (int idx = 0; idx < strlen(string); ++idx) {
    w=Font::Draw(string[idx], -xoffset+x,2);
    if (w>0) x=x+w+1;
    else if (w == 0) x+=2;
  }

  if (xoffset) delay(200);
  else delay(500);
  
  xoffset+=1;
  if (x<xoffset) xoffset = 0;
}


