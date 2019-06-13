from __future__ import print_function
import os
import arcpy

inputdir = "D:/Avi/TSX Flood Mapping/HHVV/isoclusterclass"
outputdir = "D:/Avi/TSX Flood Mapping/HHVV/isoclusterclasspoly"

for file in os.listdir(inputdir):
	if file.endswith(".tif"):
	    print('Currently convertíng {0}'.format(file))
	    name, daty = file.split('.')
	    arcpy.RasterToPolygon_conversion(inputdir+"/"+file, outputdir+"/"+name+".shp", "NO_SIMPLIFY",
                                  "VALUE")