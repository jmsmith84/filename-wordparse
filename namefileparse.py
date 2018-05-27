#!/usr/bin/env python
import os
import sys
import operator
import re
import argparse
from collections import defaultdict
###################################
def parseCmdArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--name', help='Look only for specific name')
    parser.add_argument('--min', type=int, help='Display only results with at least MIN found')
    args = parser.parse_args()
    args.name = args.name.lower()
    args.name = args.name.strip()
    return args

def collectWordCombos(words):
    list = []
    combo = ''
    x = 0
    for word in words:
        word = word.strip()
        match = re.search("^[a-z]+$", word)
        if match:
            if combo:
                combo += ' ' + word
            else:
                combo = word

            x += 1
            if x == 2:
                x = 1
                if combo not in ignoreCombos:
                    list.append(combo)
                combo = word
    return list

def displayFindings(groups):
    print("\nResults:")
    sortedlist = sorted(groups.items(), key=operator.itemgetter(1))
    for i in sortedlist:
        if i[1] >= minCutoff:
            if not args.name or (args.name and i[0] == args.name):
                print("%s [%d]" % (i[0], i[1]))

def cleanSplitWords(basename):
    cleaned = basename.replace('_', ' ')
    cleaned = cleaned.replace('-', ' ')
    cleaned = cleaned.replace('.', ' ')
    cleaned = cleaned.strip()
    cleaned = cleaned.lower()
    printDebug("cleaned: %s" % cleaned)
    return cleaned.split(' ')
###################################
args = parseCmdArgs()
debug = args.debug
minCutoff = args.min or 1
ignoreExts = []
ignoreCombos = []
groups = defaultdict(list)
initialdir = os.getcwd()

def printDebug(string):
    if args.debug:
        print(string)

for path, directories, files in os.walk(initialdir):
    for file in files:
         basename, ext = os.path.splitext(file)
         ext = ext.lstrip('.')
         if ext not in ignoreExts:
             printDebug("-found: %s.%s" % (basename, ext))

             words = cleanSplitWords(basename)
             combos = collectWordCombos(words)

             for combo in combos:
                 if args.name and combo == args.name:
                     print(os.path.join(path, file))

                 if not groups[combo]:
                    groups[combo] = 1
                 else:
                    groups[combo] += 1

displayFindings(groups)
