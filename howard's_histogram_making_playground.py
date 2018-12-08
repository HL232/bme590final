import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
import cv2
import os


def plot(image_array, title=''):
    plt.imshow(image_array, cmap=plt.cm.gray)
    plt.title(title)
    plt.axis('off')
    plt.show()
    return


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imread(dog_source, as_gray=False)
plot(dog_image, 'Normal Image')

# Histogram
'''
plt.hist(dog_image.ravel(), bins=256, range=[0,1], color='black')
plt.xlabel('Normalized Pixel Intensity')
plt.ylabel('Number of Pixels')
plt.xlim(0, 1)
plt.savefig("./temp.png")
plt.show()
'''

color = ('r', 'g', 'b')
for i, col in enumerate(color):
    histr = cv2.calcHist([dog_image], [i], None, [256], [0, 255])
    plt.plot(histr, color=col)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Number of Pixels')
    plt.xlim([0, 256])
plt.savefig("./temp.png")
plt.show()


temp = imread('temp.png')
os.remove("temp.png")
plt.imshow(temp)
plt.axis('off')
plt.show()
