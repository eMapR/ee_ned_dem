# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:33:11 2017

@author: braatenj
"""

import os
import sys
import fnmatch
import subprocess


arg = sys.argv
searchDir = arg[1]
vrtFile = arg[2]
search = arg[3]


#searchDir = '/vol/v2/conus_tiles/tiles_topo/'
#vrtFile = '/vol/v2/conus_tiles/vrts/ned_dem_ee_conus_20170501_elevation.vrt'
#search = '*ned_dem_ee_conus_20170501_elevation.bsq'

if searchDir[-1] != '/':
  searchDir += '/'

bsqs = []  
for root, dirnames, filenames in os.walk(searchDir):
  for filename in fnmatch.filter(filenames, search):
    bsqs.append(os.path.join(root, filename))

# check to make sure that total number of tiles and the tiles sizes are correct
nbsqs = len(bsqs)
if nbsqs != 2319:
  print('Warning - there are not 2319 bsq files in the provided directory')
  print('    ...there are '+str(nbsqs))  
  raise SystemExit

fileSize = [os.path.getsize(bsq) for bsq in bsqs]
if (len(set(fileSize)) > 1):
  print('Warning - all of the files are not the same size')
  print('    ...there are possibly incomplete files')  
  raise SystemExit
else:
  print('Everything checks out!')
  print('    ...making VRT file')

# make a list of tile bsqs 
tileListFile = vrtFile.replace('.vrt', '_filelist.txt')
tileList = open(tileListFile, 'w')
for bsq in bsqs:
  tileList.write(bsq+'\n')
tileList.close()

# create vrt
cmd = 'gdalbuildvrt -vrtnodata -9999 -hidenodata -input_file_list '+tileListFile+' '+vrtFile
subprocess.call(cmd, shell=True)

#os.remove(tileListFile)
