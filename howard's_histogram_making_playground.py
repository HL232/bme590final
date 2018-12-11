from processing import Processing
import matplotlib.pyplot as plt
import imageio

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

hist_image, time = P.hist_eq()
plot(hist_image, 'Hist Equalization')
plot(P.histogram(hist_image), 'Histogram Hist Eq.')
print('Gray Hist Eq. Process time: ' + str(time) + ' ms')

contrast_stretch_image,time = P.contrast_stretch()
plot(contrast_stretch_image, 'Contrast Stretch Default')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch')
print('Gray Con. Stretch 1 Process time: ' + str(time) + ' ms')


contrast_stretch_image, time = P.contrast_stretch((35, 65))
plot(contrast_stretch_image, 'Contrast Stretch Different')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch 2')
print('Gray Con. Stretch 2 Process time: ' + str(time) + ' ms')

log_comp, time = P.log_compression()
plot(log_comp, 'Log Compression Default')
plot(P.histogram(log_comp), 'Histogram Log Comp.')
print('Gray log comp Process time: ' + str(time) + ' ms')

try:
    reverse_vid, time = P.reverse_video()
    plot(reverse_vid, 'Reverse Video')
    plot(P.histogram(reverse_vid), 'Histogram Reverse Vid')
    print('Gray reverse vid Process time: ' + str(time) + ' ms')

except ValueError:
    print('Reverse video is grayscale only!')

blur, time = P.blur()
plot(blur, 'Blur')
plot(P.histogram(blur), 'Histogram blur')
print('Gray blur Process time: ' + str(time) + ' ms')

sharpen, time = P.sharpen()
plot(sharpen, 'Sharpen')
plot(P.histogram(sharpen), 'Histogram sharpen')
print('Gray sharpen Process time: ' + str(time) + ' ms')


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


hist_image, time = P.hist_eq()
plot(hist_image, 'Hist Equalization')
plot(P.histogram(hist_image), 'Histogram Hist Eq.')
print('Color Hist Eq. Process time: ' + str(time) + ' ms')

contrast_stretch_image, time = P.contrast_stretch()
plot(contrast_stretch_image, 'Contrast Stretch Default')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch')
print('Color Con. Stretch 1 Process time: ' + str(time) + ' ms')


contrast_stretch_image, time = P.contrast_stretch((35, 65))
plot(contrast_stretch_image, 'Contrast Stretch Different')
plot(P.histogram(contrast_stretch_image), 'Histogram Contrast Stretch 2')
print('Color Con. Stretch 2 Process time: ' + str(time) + ' ms')

log_comp, time = P.log_compression()
plot(log_comp, 'Log Compression Default')
plot(P.histogram(log_comp), 'Histogram Log Comp.')
print('Color log comp Process time: ' + str(time) + ' ms')

try:
    reverse_vid, time = P.reverse_video()
    plot(reverse_vid, 'Reverse Video')
    plot(P.histogram(reverse_vid), 'Histogram Reverse Vid')
    print('Color reverse vid Process time: ' + str(time) + ' ms')

except ValueError:
    print('Reverse video is grayscale only!')

blur, time = P.blur()
plot(blur, 'Blur')
plot(P.histogram(blur), 'Histogram blur')
print('Color blur Process time: ' + str(time) + ' ms')

sharpen, time = P.sharpen()
plot(sharpen, 'Sharpen')
plot(P.histogram(sharpen), 'Histogram sharpen')
print('Color sharpen Process time: ' + str(time) + ' ms')