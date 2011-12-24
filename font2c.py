#!/usr/bin/env python

from optmatch import OptionMatcher, optmatcher, optset
import json

cheader = """
extern uint8_t Glyph_ASCII_Offset;
extern uint8_t Glyphs_Count;
extern uint8_t Glyphs[][3];
"""

class Font2C(OptionMatcher):
    @optmatcher
    def main( self, fontJsonFile, noHeaderFlag=False):
        glyphs = self.load_glyphs(fontJsonFile)

        asciivals = glyphs.keys()
        asciivals.sort()
        asciioffset = asciivals[0]

        if not noHeaderFlag:
            print '/* .h */'
            print cheader

        print '/* .c */'
        print 'uint8_t Glyph_ASCII_Offset = ', asciioffset, ';'
        print 'uint8_t Glyphs_Count = ', asciivals[-1]-asciivals[0], ';'

        print 'uint8_t Glyphs[][3] = {'

        cnt = 0
        while cnt + asciioffset <= asciivals[-1]:
            asciival = cnt + asciioffset
            if asciival in asciivals:
                bbb = glyphs[asciival]
                print '    { %s,%s,%s }, '%(hex(bbb[0]), hex(bbb[1]), hex(bbb[2])),
                print '/*', unichr(asciival),'*/'
            else:
                print '    { 0xff,0xff,0xff }, ',
                print '/*', unichr(asciival),'*/'
            cnt+=1

        print '};'

    def load_glyphs(self, fontJsonFile):
        f = open(fontJsonFile)
        font = None
        with f:
            font = json.loads(f.read())

        keys = font.keys()
        """
        glyphs maps int => [byte0, byte1, byte2]

          byte0 encodes: w:2 h:2 row[0]:4
          byte1 encodes row[1]:4 row[2]:4
          byte3 encodes row[3]:4 row[4]:4

        w is encoded as 1-offset int, e.g. 2 is stored as 1 (1+1=2)
        h is encoded as 2-offset int, e.g. 4 is stored as 2 (2+2=4)

        for now it is hard coded that each glyph is no
        more than 4x5.
        """
        glyphs = {}
        spacing = 1
        for key in keys:
                if key == 'letterspace':
                    spacing = int(font[key])
                else:
                    try:
                        ascii = int(key)

                        # not sure how to handle unicode chars yet
                        if ascii > 127:
                            continue

                        rows = font[key][7:7+5]
                        rows = map(lambda x:(x>>2)&0x0F, rows)
                        height = 0
                        width = 0
                        for row in rows:
                            if row:
                                height += 1
                            mask = 0x8;
                            w = 4
                            while not row&mask and mask:
                                w-=1
                                mask = mask>>1
                            width = max(width,w)
                        w = width - 1
                        h = height - 2

                        byte0 = (w<<6) | (h<<4) | rows[0]
                        byte1 = (rows[1]<<4) | rows[2]
                        byte2 = (rows[3]<<4) | rows[4]

                        glyphs[ascii] = map(lambda x: x&0xFF,[byte0, byte1, byte2])
                        #print unichr(ascii), width,'x',height,hex(byte0),hex(byte1),hex(byte2)
                    except ValueError:
                        # ignore non-ascii values such as copy and name
                        pass
        return glyphs

if __name__ == '__main__':
    import sys
    sys.exit(Font2C().process(sys.argv))
