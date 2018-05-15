#!/usr/bin/env python
import os
import sys
import operator
import re
from collections import defaultdict

minCutoff = 3
groups = defaultdict(list)
initialdir = os.getcwd()

def collectWordCombos(words):
    list = []
    combo = ''
    x = 0
    for word in words:
        match = re.search("^[a-z]+$", word)
        if match:
            combo += ' ' + word
            x += 1
            if x == 2:
                x = 0
                list.append(combo)
                combo = ''
    return list

def displayFindings(groups):
    sortedlist = sorted(groups.items(), key=operator.itemgetter(1))

    for i in sortedlist:
        if i[1] >= minCutoff:
            print ("%s [%d]" % (i[0], i[1]))


for path, directories, files in os.walk(initialdir):
    for file in files:
         basename, ext = os.path.splitext(file)
         print("-found: %s" % basename)
         cleaned = basename.replace('_', ' ')
         cleaned = cleaned.replace('-', ' ')
         cleaned = cleaned.strip()
         cleaned = cleaned.lower()

         #print("cleaned: %s" % cleaned)
         words = cleaned.split(' ')
         combos = collectWordCombos(words)

         for combo in combos:
             if not groups[combo]:
                groups[combo] = 1
             else:
                groups[combo] += 1

displayFindings(groups)
