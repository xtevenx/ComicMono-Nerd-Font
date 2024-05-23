"""
Generates the Comic Mono font files based on Comic Shanns font.

Based on:
- monospacifier: https://github.com/cpitclaudel/monospacifier/blob/master/monospacifier.py
- YosemiteAndElCapitanSystemFontPatcher: https://github.com/dtinth/YosemiteAndElCapitanSystemFontPatcher/blob/master/bin/patch
"""

import sys
import unicodedata

import fontforge
import psMat


def height(font):
    return float(font.capHeight)


def adjust_height(source, template, scale):
    source.selection.all()
    source.transform(psMat.scale(height(template) / height(source)))
    for attr in [
            'ascent',
            'descent',
            'hhea_ascent',
            'hhea_ascent_add',
            'hhea_linegap',
            'hhea_descent',
            'hhea_descent_add',
            'os2_winascent',
            'os2_winascent_add',
            'os2_windescent',
            'os2_windescent_add',
            'os2_typoascent',
            'os2_typoascent_add',
            'os2_typodescent',
            'os2_typodescent_add',
    ]:
        setattr(source, attr, getattr(template, attr))
    source.transform(psMat.scale(scale))


font = fontforge.open('./comic-shanns/v2/comic shanns.otf')
ref = fontforge.open('./Cousine-Regular.ttf')
for g in font.glyphs():
    uni = g.unicode
    category = unicodedata.category(chr(uni)) if 0 <= uni <= sys.maxunicode else None
    if g.width > 0 and category not in ['Mn', 'Mc', 'Me']:
        target_width = 550  # avg width of chars
        if g.width != target_width:
            delta = target_width - g.width
            g.left_side_bearing = round(g.left_side_bearing + delta / 2)
            g.right_side_bearing = round(g.right_side_bearing + delta - g.left_side_bearing)

font.familyname = 'ComicMono'
font.version = '2.0.0'
font.comment = 'https://github.com/xtevenx/ComicMonoNF'
font.copyright = 'https://github.com/xtevenx/ComicMonoNF/blob/master/LICENSE'

adjust_height(font, ref, 1.0)
font.sfnt_names = []  # get rid of 'Prefered Name' etc.
font.fontname = 'ComicMono-Regular'
font.fullname = 'ComicMono Regular'
font.generate('ComicMono-Regular.ttf')

font.selection.all()
font.fontname = 'ComicMono-Bold'
font.fullname = 'ComicMono Bold'
font.weight = 'Bold'
font.changeWeight(32, "LCG", 0, 0, "squish")
font.generate('ComicMono-Bold.ttf')
