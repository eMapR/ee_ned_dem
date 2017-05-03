# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 17:07:46 2017

@author: braatenj
"""

import os
import sys
import fnmatch
import subprocess
import multiprocessing


def run_cmd(cmd):
  print(cmd)  
  return subprocess.call(cmd, shell=True)


arg = sys.argv
searchDir = arg[1]
topoType = arg[2]

#searchDir = '/vol/v2/conus_tiles/topo_tiles/'
#topoType = 'slope'

if searchDir[-1] != '/':
  searchDir += '/'

bsqs = []  
for root, dirnames, filenames in os.walk(searchDir):
  for filename in fnmatch.filter(filenames, '*elevation.bsq'):
    bsqs.append(os.path.join(root, filename))

# check to make sure that total number of tiles and the tiles sizes are correct
nbsqs = len(bsqs)
if nbsqs != 2319:
  print('Warning - there are not 2319 bsq files in the provided directory')
  print('    ...there are '+str(nbsqs))  
  raise SystemExit

if topoType == 'slope': 
  cmdList = ['gdaldem slope '+bsq+' '+bsq.replace('elevation.bsq', 'slope.bsq')+' -compute_edges -q -of ENVI' for bsq in bsqs]

if topoType == 'aspect': 
  cmdList = ['gdaldem aspect '+bsq+' '+bsq.replace('elevation.bsq', 'aspect.bsq')+' -zero_for_flat -compute_edges -q -of ENVI' for bsq in bsqs]


# run the commands in parallel 
pool = multiprocessing.Pool(processes=10)
pool.map(run_cmd, cmdList)  
pool.close()


