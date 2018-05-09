# DISCLAIMER --
# Not part of the project, just a tool I am going to use to speed up coding
import sys
import re

print 'WARNING: This script may crash on excessively large files as it reads the entire file into memory!'
if sys.argv[0] == 'dictify':
    fname = sys.argv[1]
    f = open(fname, 'rw')
    sbuf = f.read()
    f.close()
    strarr = sbuf.split('\n')
    matches = []
    for string in strarr:
        matches.append(re.match('\w+\s=\s.+', string))
