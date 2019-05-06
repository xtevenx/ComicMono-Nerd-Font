#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Update the glyph metrics so that they all really have the same size."""

# Based on
# - monospacifier: https://github.com/cpitclaudel/monospacifier/blob/master/monospacifier.py
# - YosemiteAndElCapitanSystemFontPatcher: https://github.com/dtinth/YosemiteAndElCapitanSystemFontPatcher/blob/master/bin/patch

import os
import re
import sys

reload(sys)
sys.setdefaultencoding('UTF8')

import fontforge
import psMat
import unicodedata

def height(font):
    return float(font.capHeight)

def adjust_height(source, template):
    source.selection.all()
    source.transform(psMat.scale(height(template) / height(source)))
    for attr in ['ascent', 'descent',
                'hhea_ascent', 'hhea_ascent_add',
                'hhea_linegap',
                'hhea_descent', 'hhea_descent_add',
                'os2_winascent', 'os2_winascent_add',
                'os2_windescent', 'os2_windescent_add',
                'os2_typoascent', 'os2_typoascent_add',
                'os2_typodescent', 'os2_typodescent_add',
                ]:
        setattr(source, attr, getattr(template, attr))
    source.transform(psMat.scale(0.9))

font = fontforge.open('comic-shanns.otf')
ref = fontforge.open('vendor/Menlo.ttc')
for g in font.glyphs():
    uni = g.unicode
    category = unicodedata.category(unichr(uni)) if 0 <= uni <= sys.maxunicode else None
    if g.width > 0 and category not in ['Mn', 'Mc', 'Me']:
        target_width = 510
        if g.width != target_width:
            delta = target_width - g.width
            g.left_side_bearing += delta / 2
            g.right_side_bearing += delta - g.left_side_bearing
            g.width = target_width

adjust_height(font, ref)
font.sfnt_names = [] # Get rid of 'Prefered Name' etc.
font.fontname = 'Comic Shanns dtinth'
font.familyname = 'Comic Shanns dtinth'
font.fullname = 'Comic Shanns dtinth'
font.generate('comic-shanns-dtinth.otf')