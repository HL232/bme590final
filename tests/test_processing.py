import pytest
from processing import Processing

import matplotlib.pyplot as plt
from skimage.io import imread

# Manually testing processing.py


def plot(image_array, title):
    plt.imshow(image_array, cmap=plt.cm.gray)
    plt.title(title)
    plt.axis('off')
    plt.show()
    return


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imread(dog_source, as_gray=True)
plot(dog_image, 'Normal, Grayscale Image')

P = Processing()
plot(P.hist_eq(dog_image), 'Hist Equalization')
plot(P.contrast_stretch(dog_image), 'Contrast Streching Default')
plot(P.contrast_stretch(dog_image, (35, 65)), 'Contrast Streching (35,65)')
plot(P.log_compression(dog_image), 'Log Compression Default')
plot(P.log_compression(dog_image, 100), 'Log Compression Log=100')
plot(P.reverse_video(dog_image), 'Reverse Video')
plot(P.blur(dog_image), 'Blur default')
plot(P.blur(dog_image, 10), 'Blur Sigma = 10')
plot(P.sharpen(dog_image), 'Sharpen')
plot(P.histogram_gray(dog_image), 'Histogram of original')