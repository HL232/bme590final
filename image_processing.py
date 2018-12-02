from skimage.io import imread
import matplotlib.pyplot as plt
from skimage import exposure
import numpy as np


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imread(dog_source, as_gray=True)
plt.imshow(dog_image, cmap=plt.cm.gray)
plt.title('Normal, Grayscale Image')
plt.axis('off')
plt.show()

# Histogram Equilzation
dog_image_HE = exposure.equalize_hist(dog_image)
plt.imshow(dog_image_HE, cmap=plt.cm.gray)
plt.title('Histogram Equilzation')
plt.axis('off')
plt.show()

# Contrast Stretching
# Set what percentile of the contrast you want to eliminate below
p2, p98 = np.percentile(dog_image, (10, 90))
dog_image_rescale = exposure.rescale_intensity(dog_image, in_range=(p2, p98))
plt.imshow(dog_image_rescale, cmap=plt.cm.gray)
plt.title('Contrast Stretching')
plt.axis('off')
plt.show()

# Log Compression

# Reverse Video
