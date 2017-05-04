#!/usr/bin/env python
import sys
from obspy import read

for infile in sys.argv[1:]:
   tr = read(infile)[0]
   tr.write(infile + '.sac', format='SAC')
