from __future__ import print_function
import os
import arcpy
from arcpy.sa import *

inputdir = "D:/Avi/TSX Flood Mapping/HHVVseg_k_db"
outputdir = "D:/Avi/TSX Flood Mapping/HHVV/isoclusterclass"

for file in os.listdir(inputdir):
	if file.endswith(".tif"):
	    print('Currently classifying {0}'.format(file))
            #calculate statistics
            outUnsupervised = IsoClusterUnsupervisedClassification(inputdir+"/"+file, 4, 20, 10)
            outUnsupervised.save(outputdir+"/"+file)
            print('done!')