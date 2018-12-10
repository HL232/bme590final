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

# ***********************************************************************
# Grayscale TESTING STARTS HERE *********************************************
# ***********************************************************************


dog_source = 'https://thumbs.dreamstime.com/b' \
             '/grayscale-photography-short-coated-dog-83077538.jpg'
dog_image = imageio.imread(dog_source, format="JPG")
plt.imshow(dog_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')
plt.show()
P = Processing(dog_image)
plot(P.histogram(dog_image), 'Histogram Original')

hist_image = P.hist_eq()[0]
plot(hist_image, 'Hist Equalization')
plot(P.histogram(hist_image), 'Histogram Hist Eq.')

contrast_stretch_image = P.contrast_stretch()[0]
plot(contrast_stretch_image, 'Contrast Stretch Default')


contrast_stretch_image = P.contrast_stretch((35, 65))[0]
plot(contrast_stretch_image, 'Contrast Stretch Different')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch 2')

log_comp = P.log_compression()[0]
plot(log_comp, 'Log Compression Default')
plot(P.histogram(log_comp), 'Histogram Log Comp.')

try:
    reverse_vid = P.reverse_video()[0]
    plot(reverse_vid, 'Reverse Video')
    plot(P.histogram(reverse_vid), 'Histogram Reverse Vid')


except ValueError:
    print('Reverse video is grayscale only!')

blur = P.blur()[0]
plot(blur, 'Blur')
plot(P.histogram(blur), 'Histogram blur')

sharpen = P.sharpen()[0]
plot(sharpen, 'Sharpen')
plot(P.histogram(sharpen), 'Histogram sharpen')


# ***********************************************************************
# COLOR TESTING STARTS HERE *********************************************
# ***********************************************************************

dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_image = imageio.imread(dog_source, format="JPG")
plt.imshow(dog_image)
plt.title('Original Image')
plt.axis('off')
plt.show()
P = Processing(dog_image)
plot(P.histogram(dog_image), 'Histogram Original')


contrast_stretch_image = P.contrast_stretch()[0]
plot(contrast_stretch_image, 'Contrast Stretch Default')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch 1')

contrast_stretch_image = P.contrast_stretch((35, 65))[0]
plot(contrast_stretch_image, 'Contrast Stretch Different')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch 2')

log_comp = P.log_compression()[0]
plot(log_comp, 'Log Compression Default')
plot(P.histogram(log_comp), 'Histogram Log Comp.')

try:
    reverse_vid = P.reverse_video()[0]
    plot(reverse_vid, 'Reverse Video')
    plot(P.histogram(reverse_vid), 'Histogram Reverse Vid')


except ValueError:
    print('Reverse video is grayscale only!')

blur = P.blur()[0]
plot(blur, 'Blur')
plot(P.histogram(blur), 'Histogram blur')

sharpen = P.sharpen()[0]
plot(sharpen, 'Sharpen')
plot(P.histogram(sharpen), 'Histogram sharpen')
