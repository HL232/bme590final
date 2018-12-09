from processing import Processing
import matplotlib.pyplot as plt
import imageio
import numpy as np

# Manually testing processing.py


def plot(image_array, title):
    plt.imshow(image_array)
    plt.title(title)
    plt.axis('off')
    plt.show()
    return


dog_source = 'https://thumbs.dreamstime.com/b' \
             '/grayscale-photography-short-coated-dog-83077538.jpg'
dog_image = imageio.imread(dog_source, format="JPG")
plt.imshow(dog_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()
P = Processing(dog_image)


hist_image = P.hist_eq()[0]
plot(hist_image, 'Hist Equalization')

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
dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imageio.imread(dog_source, format="JPG")
plt.imshow(dog_image)
plt.title('Original Image')
plt.axis('off')
plt.show()
P = Processing(dog_image)


hist_image = P.hist_eq()[0]
plot(hist_image, 'Hist Equalization')

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