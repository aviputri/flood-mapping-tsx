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

# The input 4-band TSX image
image = r'raw_img/09K0153_20140501T084638_TSX.tif'

#convert image to Np array
img = io.imread(image, as_gray=False, plugin="gdal")

# Run the quick shift segmentation
#segments = quickshift(img, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5)
#segments = slic(img, n_segments=100, compactness=10.0, max_iter=10, sigma=0, spacing=None, multichannel=False, 
#	convert2lab=None, enforce_connectivity=True, min_size_factor=0.5, max_size_factor=3, slic_zero=False)
segments = slic(img, n_segments=500, multichannel=False)
print("Quickshift number of segments: %d" % len(np.unique(segments)))

# View the segments via Python
# plt.imshow(segments)
# IDK doesn't work in this PC

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

b1 = segments[:,:,1].astype('uint32')
b2 = segments[:,:,2].astype('uint32')
b3 = segments[:,:,3].astype('uint32')
b4 = segments[:,:,4].astype('uint32')

result_raster = "img/09K0153_20140501T084638_TSX_b1.tif"
new_dataset = rasterio.open(result_raster, 'w', driver='GTiff',
	height = b1.shape[0], width = b1.shape[1],
	count=1, dtype=b1.dtype,
	crs=proj_init,
	transform=transform)

new_dataset.write(b1, 1)
new_dataset.close()