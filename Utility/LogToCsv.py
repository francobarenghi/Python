# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 12:54:45 2010

@author: FrancoB
"""

__author__ = 'FrancoB'

from optparse import OptionParser


def convert(sourceFilename, destFilename):
    fin = open(sourceFilename, "r")
    fout = open(destFilename, "w")
    for line in fin:
        newLine = convertLine(line)
        if newLine is not None:
            fout.write(newLine)
    fin.close()
    fout.close()

def convertLine(line):
    try:
        i = int(line[:2])
    except:
        # skip comments
        return None
    line = str(line).replace('\r', '; ')
    line = str(line).replace('.', ',')
    newLine = str(line).replace('>', ' ')
    return newLine


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="filename",
        help="read data from FILENAME")
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        print "reading %s..." % args[0]

    convert(args[0], "C:\\temp\\pippo.csv")


if __name__ == "__main__":
    main()