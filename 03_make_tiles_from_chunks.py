# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:33:11 2017

@author: braatenj
"""

import os
import fnmatch
import json
import sys
import subprocess
import multiprocessing



def run_cmd(cmd):
  print(cmd)  
  return subprocess.call(cmd, shell=True)

def get_tile_id_and_coords(feature):          
  xmax = feature['properties']['xmax']
  xmin = feature['properties']['xmin']
  ymax = feature['properties']['ymax']
  ymin = feature['properties']['ymin']
  coords = ' '.join([str(coord) for coord in [xmin,ymax,xmax,ymin]])
   
  # prepend 0's to tileID so they all have 4 digits
  tileID = str(feature['properties']['id'])
  zeros = '0'*(4-len(tileID))
  tileID = zeros+tileID        
  
  return (coords, tileID) 


# get the arguments
args = sys.argv
chunkDir = args[1]
outDir = args[2]  
tileFile = args[3]
name = args[4]
nodata = args[5]  
proj = args[6]


#chunkDir = '/vol/v2/conus_tiles/staging/gdrive/'
#outDir = '/vol/v2/conus_tiles/tiles_topo/'
#tileFile = '/vol/v1/general_files/datasets/spatial_data/conus_tile_system/conus_tile_system_15_sub_epsg5070.geojson'
#name = 'ned_dem_ee_conus_20170501_elevation'
#nodata = 'nan'
#proj = 'EPSG:5070'



# make sure path parts are right
if chunkDir[-1] != '/':
  chunkDir += '/'
if outDir[-1] != '/':
  outDir += '/'


# find the tif chunks
tifs = []
for root, dirnames, filenames in os.walk(chunkDir):
  for filename in fnmatch.filter(filenames, '*.tif'):
    tifs.append(os.path.join(root, filename))
    
    
# make a list of tile tifs
vrtFile = chunkDir+name+'_staging.vrt'
tileListFile = vrtFile.replace('.vrt', '_filelist.txt')
tileList = open(tileListFile, 'w')
for tif in tifs:
  tileList.write(tif+'\n')
tileList.close()


# create vrt
cmd = 'gdalbuildvrt -srcnodata '+nodata+' -vrtnodata -9999 -input_file_list '+tileListFile+' '+vrtFile
subprocess.call(cmd, shell=True)


# load the tile features
with open(tileFile) as f:
  features = json.load(f)['features']
 
 
# make a list of all the gdal_translate commands needed for the ee conus chunk
cmdList = []
for feature in features:   
  coords, tileID = get_tile_id_and_coords(feature)
  tileOutDir = outDir+tileID
  if not os.path.isdir(tileOutDir):
    os.mkdir(tileOutDir)
  
  outFile = tileOutDir+'/'+tileID+'_'+name+'.bsq'
  cmd = 'gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -of ENVI -a_nodata none -a_srs '+proj+' -projwin '+coords+' '+ vrtFile + ' ' + outFile    
  cmdList.append(cmd)  


# run the commands in parallel 
pool = multiprocessing.Pool(processes=10)
pool.map(run_cmd, cmdList)  
pool.close()






