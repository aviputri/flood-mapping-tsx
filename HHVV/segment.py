from __future__ import print_function
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

# The input 4-band TSX image
image = r'raw_img/09K0153_20140501T084638_TSX.tif'

#convert image to Np array
img = io.imread(image, as_gray=False, plugin="gdal")

# Run the quick shift segmentation
segments = quickshift(img, kernel_size=3, convert2lab=False, max_dist=6, ratio=0.5)
print("Quickshift number of segments: %d" % len(np.unique(segments)))

# View the segments via Python
plt.imshow(segments)
