from __future__ import print_function
from osgeo import gdal
import rasterio
from rasterio.transform import from_origin
import cv2
import PyQt5
import matplotlib
matplotlib.get_backend()
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from skimage import io
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color

"""
def image_show(image, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    plt.show()
    return fig, ax
"""
#doesn't work because plt can only show RGB data with 0..1 for float and 0..255 for integers

image_path = 'raw_img/09K0153_20140501T084638_TSX.tif'
image = io.imread(image_path, as_gray=False, plugin="gdal")
#plt.imshow(image);
#plt.show()

