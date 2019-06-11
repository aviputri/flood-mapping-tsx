from __future__ import print_function
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np

from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

image = r'C:\path\to\my\geotiff.tif'
img = io.imread(image, as_grey=False, plugin="gdal")
segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)