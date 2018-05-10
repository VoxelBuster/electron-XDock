# DISCLAIMER --
# Not part of the project, just a tool I am going to use to speed up coding
import sys
import re

print 'WARNING: This script may crash on excessively large files as it reads the entire file into memory!'
if sys.argv[1] == 'dictify':
    print 'Moving global attributes into a dictionary...'
    fname = sys.argv[2]
    f = open(fname, 'r+')
    sbuf = f.read()
    strarr = sbuf.split('\n')
    kvList = []
    for x in range(len(strarr)):
        match = re.match('^\w+\s=\s.+', strarr[x])
        if match is not None:
            matchStr = match.string
            kvList.append((x, 'fields[\'' + re.compile('\s=\s').split(matchStr)[0] + '\'] = ' + re.compile('\s=\s').split(matchStr)[1]))
    strarr.insert(0, 'fields = {}\n')
    for item in kvList:
        strarr[item[0]] = item[1]
    f.truncate(0)
    for line in strarr:
        f.write(line + '\n')
    f.close()
    print 'Operation completed'

