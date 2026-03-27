# Get top/bottom limits
import fontforge
import os

fontforge.runInitScripts()
font = fontforge.activeFont()

# Work
loLimit = 0
hiLimit = 0
for glyph in font.glyphs():
    [x1,y1,x2,y2] = glyph.boundingBox()
    loLimit = min(loLimit, y1)
    hiLimit = max(hiLimit, y2)

# Output data
file = open('~topbottom.log', 'w')
print(f"lo={loLimit}, hi={hiLimit}\n", file=file)
file.close()
