#!/usr/bin/env python

from optmatch import OptionMatcher, optmatcher, optset
import json

class Font2h(OptionMatcher):
    @optmatcher
    def main( self, fontJsonFile):
        print '/*'
        glyphs = self.load_glyphs(fontJsonFile)
        print '*/'

        asciivals = glyphs.keys()
        asciivals.sort()
        asciioffset = asciivals[0]

        print 'char Glyph_ASCII_offset = ', asciioffset, ';'

        print 'char Glyphs[][3] = {'
        for asciival in asciivals:
            bbb = glyphs[asciival]
            print '    { %s,%s,%s }, '%(hex(bbb[0]), hex(bbb[1]), hex(bbb[2])),
            print '/*', unichr(asciival),'*/'
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

        w and h are encoded as 2 offset integers, e.g.
        if width is 2+w and height is 2+h

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
                        #print key,rows
                        rows = map(lambda x:(x>>2)&0x0F, rows)
                        height = 0
                        width = 0
                        for row in rows:
                            if row:
                                height += 1
                            r = row
                            w = 0
                            while(r):
                                if r:
                                    w+=1
                                r = r>>1
                            width = max(width,w)
                        #print width,'x',height
                        width -= 2
                        height -= 2

                        byte0 = (width<<6) | (height<<4) | rows[0]
                        byte1 = (rows[1]<<4) | rows[2]
                        byte2 = (rows[3]<<4) | rows[4]

                        glyphs[ascii] = map(lambda x: x&0xFF,[byte0, byte1, byte2])
                        #print unichr(ascii), hex(byte0),hex(byte1),hex(byte2)
                    except ValueError:
                        # ignore non-ascii values such as copy and name
                        pass
        return glyphs

if __name__ == '__main__':
    import sys
    sys.exit(Font2h().process(sys.argv))
