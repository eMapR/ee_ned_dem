# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:43:51 2017

@author: braatenj
"""

import subprocess
import sys
import os

args = sys.argv
inDEM = args[1]
outDir = args[2]

#inDEM = '/vol/v2/conus_tiles/vrts/ned_dem_ee_conus_20170501_elevation.vrt'
#outDir = '/vol/v2/conus_tiles/staging/ned_dem/'


if outDir[-1] != '/':
  outDir += '/'

outDEM = outDir+os.path.basename(inDEM)
outSlope =  outDEM.replace('elevation.vrt', 'slope.bsq')
outAspect = outDEM.replace('elevation.vrt', 'aspect.bsq')
outTPI =    outDEM.replace('elevation.vrt', 'tpi.bsq')

# create vrt
cmd = 'gdalbuildvrt -vrtnodata -9999 '+outDEM+' '+inDEM
subprocess.call(cmd, shell=True)

cmdSlope = 'gdaldem slope '+outDEM+' '+outSlope+' -compute_edges -q -of ENVI'
cmdAspect = 'gdaldem aspect '+outDEM+' '+outAspect+' -compute_edges -q -of ENVI'  #-zero_for_flat
cmdTPI = 'gdaldem TPI '+outDEM+' '+outTPI+' -compute_edges -q -of ENVI'


subprocess.call(cmdSlope, shell=True)
subprocess.call(cmdAspect, shell=True)
subprocess.call(cmdTPI, shell=True)
