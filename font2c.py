#!/usr/bin/env python
"""
This script reads json produced by:

    http://www.pentacom.jp/pentacom/bitfontmaker2/

and produces .h and .c files suitable for the Arduino environment.

The maximum size of each glyph is 8x8, represented as an 8 element byte array.

In addition to the glyph, yoffset and glyph width is stored, so the proportional
rendering is possible, as is descenders. Positive yoffset moves the glyph upwards.

Descenders are automatically detected - the script pixels below the 12th row
(origin top left) as descenders.

Note that the script simply scans the rows top-down, stopping when 8 rows,
starting with the first non-zero row, has been read. The 8 columns are read
starting from column 2.
"""

from optmatch import OptionMatcher, optmatcher, optset
import json

cheader = """
extern uint8_t Glyph_ASCII_Offset;
extern uint8_t Glyphs_Count;
"""

class Glyph(object):
    @classmethod
    def unknownGlyph(self, asciiChar):
        return Glyph(asciiChar, [0xff]*8)

    def __init__(self, asciiChar, jrows):
        super(Glyph, self).__init__()

        self.asciiChar = asciiChar
        self.rows = []
        rowcnt = 0
        rowstep = 0
        # extract the first 8 rows, starting with the first non-empty row
        # XXX handle when glyph is less than 4 rows tall
        for rowidx, row in enumerate(jrows):
            if row:
                rowstep = 1
            if rowstep:
                self.rows.append(row)
                rowcnt += rowstep
                if rowcnt >= 8:
                    if rowidx > 11:
                        self.yoffset = 11-rowidx
                    break

        # since left is LSB, throw away the first 2 columns by bit shifting
        # lower. Then throw away the the rest by AND'ing with 0x00FF
        maxrowval = -1
        for idx in xrange(len(self.rows)):
            row = self.rows[idx]
            row = row >> 2
            row = row & 0xFF
            if row > maxrowval:
                maxrowval = row
            self.rows[idx] = row

        self.width = 0
        while maxrowval:
            self.width += 1
            maxrowval = maxrowval >> 1

        print '//encoded glyph', self.asciiChar, 'width:',self.width, 'yoffset:', self.yoffset

    @classmethod
    def cStructDef(self):
        return ""
        return """
typedef struct {
    uint8_t width;
    uint8_t yoffset;
    uint8_t rows[8];
} Glyph_t;
            """

    @classmethod
    def cType(self):
        return 'Glyph_t'

    def printCDef(self):
        """
        Prints out the C init'd code to initalize a struct as defined in 
        cStructDef
        """
        print '{ /*',self.asciiChar,'*/'
        print ' ',self.width,','
        print ' ',self.yoffset,','
        print ' {'
        for row in self.rows:
            print '  ',row,','
        print ' }'
        print '}'

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
            print Glyph.cStructDef()
            print 'extern',Glyph.cType(),' Glyphs[];'

        print '/* .c */'
        print 'uint8_t Glyph_ASCII_Offset = ', asciioffset, ';'
        print 'uint8_t Glyphs_Count = ', asciivals[-1]-asciivals[0]+1, ';'

        print Glyph.cType(),'Glyphs[] = {'

        cnt = 0
        while cnt + asciioffset <= asciivals[-1]:
            asciival = cnt + asciioffset
            glyph = None
            if asciival in asciivals:
                glyph = glyphs[asciival]
            else:
                glyph = Glyph.unknownGlyph(chr(asciival))
            glyph.printCDef()
            print '  ,'
            cnt+=1

        print '};'

    def load_glyphs(self, fontJsonFile):
        f = open(fontJsonFile)
        font = None
        with f:
            font = json.loads(f.read())

        keys = font.keys()
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


                        glyph = Glyph(chr(ascii), font[key])
                        glyphs[ascii] = glyph
                    except ValueError:
                        # ignore non-ascii values such as copy and name
                        pass
        return glyphs

if __name__ == '__main__':
    import sys
    sys.exit(Font2C().process(sys.argv))
