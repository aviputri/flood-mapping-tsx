#the concept of skimage segmentation is different, guys
#cannot use it

from __future__ import print_function
from osgeo import gdal
#import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage.segmentation import felzenszwalb, slic, quickshift, random_walker
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import rasterio
from rasterio.transform import from_origin
import cv2
import PyQt5
import matplotlib
matplotlib.get_backend()
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
#%matplotlib inline
from scipy import ndimage
from sklearn.cluster import KMeans

# The input 4-band TSX image
image = 'raw_img/09K0153_20140501T084638_TSX.tif'

#convert image to Np array
img = io.imread(image, as_gray=False, plugin="gdal")

img_n = img.reshape(img.shape[0]*img.shape[1], img.shape[2])

kmeans = KMeans(n_clusters=10, random_state=0).fit(img_n)
img2show = kmeans.cluster_centers_[kmeans.labels_]

cluster_img = img2show.reshape(img.shape[0], img.shape[1], img.shape[2])

#the origin of Rasterio is the coordinate of the Southwest edge of the raster file
#this should be based on the source raster that is used
#transform = from_origin(longitude, latitude, X resolution, Y resolution)
#feel free to modify the long, lat, and resolutions

#get the source raster origin (= the southwest corner of the raster)
imgdal = gdal.Open(image, gdal.GA_ReadOnly)
trans = imgdal.GetGeoTransform()
xRes = trans[1]
yRes = trans[5]
xOrigin = trans[0]
yOrigin = trans[3] + (imgdal.RasterYSize)*yRes
xSize = imgdal.RasterXSize
#close gdal dataset
imgdal = None
#hence the raster origin
transform = from_origin(xOrigin, yOrigin, xRes, yRes)

#now define the CRS in rasterio (because GDAL's CRS is of different format, and IDK how to convert it w/o
# including another library)
imgras = rasterio.open(image)
#take the CRS
proj_init = imgras.crs
#close the raster
imgras.close()

#c = np.flipud(segments) #flip vertically
#c = c.astype('uint32')
#because rasterio writes from bottom to top

for band in range(cluster_img.shape[2]):
	b = cluster_img[:,:,band]
	b = np.flipud(b)

	result_raster = "img/09K0153_20140501T084638_TSX_b"+str(band+1)+".tif"

	new_dataset = rasterio.open(result_raster, 'w', driver='GTiff',
		height = b.shape[0], width = b.shape[1],
		count=1, dtype=b.dtype,
		crs=proj_init,
		transform=transform)

	new_dataset.write(b, 1)
	new_dataset.close()