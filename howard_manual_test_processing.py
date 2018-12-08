import pytest
from processing import Processing
import matplotlib.pyplot as plt
from skimage.io import imread
import custom_errors
import numpy as np


# Manually testing processing.py


def plot(image_array, title):
    plt.imshow(image_array)
    plt.title(title)
    plt.axis('off')
    plt.show()
    return


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imread(dog_source, as_gray=False)

P = Processing(dog_image)


plot(P.hist_eq()[0], 'Hist Equalization')
blah = P.hist_eq()[0]
print(np.amax(blah))
print(type(blah))

plot(P.contrast_stretch()[0], 'Contrast Streching Default')
blah = P.contrast_stretch()[0]
print(np.amax(blah))
print(type(blah))

plot(P.contrast_stretch((35, 65))[0], 'Contrast Streching (35,65)')
blah = P.contrast_stretch((35, 65))[0]
print(np.amax(blah))
print(type(blah))

plot(P.log_compression()[0], 'Log Compression Default')
blah = P.log_compression()[0]
print(np.amax(blah))
print(type(blah))

plot(P.log_compression(100)[0], 'Log Compression Log=100')
blah = P.log_compression(100)[0]
print(np.amax(blah))
print(type(blah))

plot(P.reverse_video()[0], 'Reverse Video')
blah = P.reverse_video()[0]
print(np.amax(blah))
print(type(blah))

plot(P.blur()[0], 'Blur default')
blah = P.blur()[0]
print(np.amax(blah))
print(type(blah))

plot(P.blur(10)[0], 'Blur Sigma = 10')
blah = P.blur()[0]
print(np.amax(blah))
print(type(blah))

plot(P.sharpen()[0], 'Sharpen')
blah = P.sharpen()[0]
print(np.amax(blah))
print(type(blah))

plot(P.histogram_gray(), 'Histogram of original')
blah = P.histogram_gray()
print(np.amax(blah))
print(type(blah))
