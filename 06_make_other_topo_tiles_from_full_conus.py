# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:01:52 2017

@author: braatenj
"""


import json
import subprocess
import multiprocessing
import sys



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



args = sys.argv
topoFile = args[1]
outDir = args[2]
name = args[3]
tileFile = args[4]
proj = args[5]

#topoFile = '/vol/v2/conus_tiles/staging/ned_dem/ned_dem_ee_conus_20170501_tpi.bsq'
#outDir = '/vol/v2/conus_tiles/tiles_topo/'
#name = 'ned_dem_ee_conus_20170501_tpi.bsq'
#tileFile = '/vol/v1/general_files/datasets/spatial_data/conus_tile_system/conus_tile_system_15_sub_epsg5070.geojson'
#proj = 'EPSG:5070'


# load the tile features
with open(tileFile) as f:
  features = json.load(f)['features']
 
 
# make a list of all the gdal_translate commands needed for the ee conus chunk
cmdList = []
for feature in features:   
  coords, tileID = get_tile_id_and_coords(feature)
  tileOutDir = outDir+tileID
  outFile = tileOutDir+'/'+tileID+'_'+name
  cmd = 'gdal_translate -q --config GDAL_DATA "/usr/lib/anaconda/share/gdal" -a_nodata none -of ENVI -a_srs ' + proj + ' -projwin '+coords+' '+ topoFile + ' ' + outFile    
  cmdList.append(cmd)  


# run the commands in parallel 
pool = multiprocessing.Pool(processes=10)
pool.map(run_cmd, cmdList)  
pool.close()

