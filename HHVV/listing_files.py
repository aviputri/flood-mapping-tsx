from __future__ import print_function
import os

inputdir = "raw_img_k_db"

for file in os.listdir(inputdir):
	if file.endswith(".tif"):
		print('File name is: {0}'.format(file))