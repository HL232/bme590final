import pytest
from processing import Processing, output_0_to_255_as_int
import matplotlib.pyplot as plt
from skimage.io import imread
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
dog_image = imread(dog_source, as_gray=True)
dog_image = output_0_to_255_as_int(dog_image)
plt.imshow(dog_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()
P = Processing(dog_image)
plot(P.histogram(dog_image), 'Histogram original')


hist_image = P.hist_eq()[0]
plot(hist_image, 'Hist Equalization')
plot(P.histogram(hist_image), 'Histogram Hist Eq')

'''
contrast_stretch_image = P.contrast_stretch()[0]

plot(contrast_stretch_image, 'Contrast Stretch Default')

contrast_stretch_image = P.contrast_stretch((35,65))[0]

plot(contrast_stretch_image, 'Contrast Stretch Different')

plot(P.log_compression()[0], 'Log Compression Default')

try:
    plot(P.reverse_video()[0], 'Reverse Video')

except ValueError:
    print('Reverse video is grayscale only!')

plot(P.blur()[0], 'Blur')

plot(P.sharpen()[0], 'Sharpen')
'''
