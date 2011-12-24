#include <Charliplexing.h>
#include <Font.h>

#include "sifontv1.h"

char display_str[181];

// returns length of string read, 0 if nothing was read
int _readstring(char *buf, uint8_t bufsize) {
  int cnt = 0;
  
  while(Serial.available() && cnt < bufsize-1) {
    do {
      int c = Serial.read();
      switch(c) {
        case '\r':
        case '\n':
        case '\t':
          c = ' ';
        default:
          buf[cnt++] = c;
      }
    } while(Serial.available());
    buf[cnt] = '\0'; 
    Serial.println(cnt);
    delay(100);
  }
  return cnt;
}
    
void setup () {  
  Serial.begin(19200);
  delay(100);
  
  LedSign::Init(); 
  Font::SetGlyphs(Glyphs, Glyph_ASCII_Offset, Glyphs_Count);
  Serial.println("ready");
}

int xoffset = 0;
boolean done;

void loop() {
  LedSign::Clear();
  int x = 0;
  int l = strlen(display_str);
  if (l) {
    for (int idx = 0; idx < l; ++idx) {
      int w=Font::Draw(display_str[idx], -xoffset+x,2);
      if (w>0) x=x+w+1;
      else if (w == 0) x = x + 3;
    }
  } else {
    Font::Draw('>', 0,2);
  }

  if (xoffset) delay(80);
  else delay(1000);
  
  xoffset+=1;
  if (x<=xoffset) {
    xoffset = 0;
    if (_readstring(display_str, sizeof display_str)) {
      Serial.print("display_str: ");
      Serial.print(display_str);
      Serial.print(" len: ");
      Serial.println(strlen(display_str));
    }
  }
}


