# -*- coding: utf-8 -*-
"""
Created on Mon May  1 20:35:20 2017

@author: braatenj
"""

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import sys
import time
import multiprocessing
from functools import partial


# define function to download tif files found in gDrive folder - called by multiprocessing.Pool().map()
def download_files(fileName, outDirPath):
  print(fileName['title'])
  getFile = drive.CreateFile({'id': fileName['id']})
  getFile.GetContentFile(outDirPath+fileName['title']) # Download file

# get the arguments
args = sys.argv
gDriveDirBase = args[1]
outDirPath = args[2]

#gDriveDirBase = 'conus_ned_dem_chunk'
#outDirPath = '/vol/v2/conus_tiles/staging/gdrive/'

if gDriveDirBase[-1] != '_':
  gDriveDirBase += '_'
  
if outDirPath[-1] != '/':
  outDirPath += '/'

gDriveDirs = []
for strip in range(0,16):
  if strip < 10:
    strip = '0'+str(strip)
  else:
    strip = str(strip)
  gDriveDirs.append(gDriveDirBase+strip)
  


os.chdir('/vol/v1/general_files/script_library/earth_engine/') #GoogleAuth looks in here for an authorization file - could pass the file as an argument and the get the os.path.dirname

# authenticate gDrive application and request access to gDrive account
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)     
                        
# find files in the specified gDrive folder
for gDriveDir in gDriveDirs:
  gDir = drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and title contains '"+gDriveDir+"'"}).GetList()
  if len(gDir) == 1: # TODO else print problem and exit
    fileList = drive.ListFile({'q': "'"+gDir[0]['id']+"' in parents and title contains '.tif'"}).GetList()
  
  # create the output folder if it does not already exist
    if not os.path.isdir(outDirPath):
      os.mkdir(outDirPath)

  # loop through downloading the files in parallel
    pool = multiprocessing.Pool(processes=3) 
    func = partial(download_files, outDirPath=outDirPath)
    pool.map(func, fileList)  

pool.close()  
  
