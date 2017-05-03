# -*- coding: utf-8 -*-
"""
Created on Tue May  2 10:51:51 2017

@author: braatenj
"""

import os
import fnmatch

searchDir = '/vol/v2/conus_tiles/tiles_topo/'
search = '*ned_dem_ee_conus_20170501*'

if searchDir[-1] != '/':
  searchDir += '/'

files = []  
for root, dirnames, filenames in os.walk(searchDir):
  for filename in fnmatch.filter(filenames, search):
    files.append(os.path.join(root, filename))

nfiles = len(files)
# number of tiles: 2319


# delete files
for fn in files:
  os.remove(fn)


# rename files
hdr = [thisFile.replace('.bsq', '.hdr') for thisFile in files]
newBsq = [thisFile.replace('.bsq', '_elevation.bsq') for thisFile in files]
newHdr = [thisFile.replace('.hdr', '_elevation.hdr') for thisFile in hdr]

for oldFile, newFile in zip(files, newBsq):
  os.rename(oldFile, newFile)
  
for oldFile, newFile in zip(hdr, newHdr):
  os.rename(oldFile, newFile)
