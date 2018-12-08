import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread


def plot(image_array, title=''):
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

# Histogram
plt.hist(dog_image.ravel(), bins=256, range=(0.0, 1.0), color='black')
plt.xlabel('Normalized Pixel Intensity')
plt.ylabel('Number of Pixels')
plt.xlim(0, 1)
plt.savefig ( "./temp.png")
plt.show()

temp = imread('temp.png')
plt.imshow(temp)
plt.axis('off')
plt.show()
