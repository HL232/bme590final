import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage import exposure
from skimage import util
from skimage import filters


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

# Histogram Equilzation
dog_image_HE = exposure.equalize_hist(dog_image)
plot(dog_image_HE, 'Histogram Equilzation')


# Contrast Stretching
# Set what percentile of the contrast you want to eliminate below
p2, p98 = np.percentile(dog_image, (10, 90))
dog_image_rescale = exposure.rescale_intensity(dog_image, in_range=(p2, p98))
plot(dog_image_rescale, 'Contrast Stretching')


# Log Compression
# I need to check this later
base = 4
dog_image_log = np.log(dog_image+1) / np.log(base)
plot(dog_image_log, 'Log Compression?')


# Reverse Video
# I think this is just inverting the image
# to do: Invert color images
dog_image_reverse = util.invert(dog_image)
plot(dog_image_reverse, 'Reverse Video?')

# Gaussian Blur
dog_image_blur = filters.gaussian(dog_image, sigma=5)
plot(dog_image_blur, 'Blurred')

# Sharpen Image
# dog_image_sharpened = filters.unsharp_mask(dog_image, radius=1, amount=1)
# You're supposed to use unsharp_mask but it doesn't seem to exist in
# skimage.filters anymore
alpha = 1
dog_image_sharpened = dog_image + alpha * (dog_image - dog_image_blur)
plot(dog_image_sharpened, 'Sharpened')

# Histogram
plt.hist(dog_image.ravel(), bins=256, range=(0.0, 1.0), color='black')
plt.xlabel('Normalized Pixel Intensity')
plt.ylabel('Number of Pixels')
plt.xlim(0, 1)
plt.savefig("./temp.png")
plt.show()

temp = imread('temp.png')
plt.imshow(temp)
plt.axis('off')
plt.show()
