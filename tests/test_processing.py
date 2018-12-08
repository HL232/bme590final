import pytest
from processing import Processing
import matplotlib.pyplot as plt
from skimage.io import imread
import custom_errors
import numpy as np


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

P = Processing(dog_image)

plot(P.hist_eq()[0], 'Hist Equalization')
plot(P.contrast_stretch()[0], 'Contrast Streching Default')
plot(P.contrast_stretch((50, 75))[0], 'Contrast Streching (dif numbers)')
plot(P.log_compression()[0], 'Log Compression Default')
plot(P.log_compression(100)[0], 'Log Compression Log=100')
plot(P.reverse_video()[0], 'Reverse Video')
plot(P.blur()[0], 'Blur default')
plot(P.blur(10)[0], 'Blur Sigma = 10')
plot(P.sharpen()[0], 'Sharpen')
plot(P.histogram_gray(), 'Histogram of original')

'''
@pytest.mark.parametrize("candidate", [
    Processing('blah'),
    Processing(3),
    Processing(2.4),
    Processing([1, 2, 3]),
    Processing((1, 3)),
    Processing(np.array([2, 3, 1, 0]))
])
def test_check_image_type(candidate):
    try:
        assert candidate._check_image_type()
    except TypeError:
        with pytest.raises(TypeError):
            candidate._check_image_type()


@pytest.mark.parametrize("candidate", [
    Processing(np.array([2, 3, 1, 0])),
    Processing(np.zeros((2, 3))),
    Processing(np.zeros((2, 3, 4))),
    Processing(np.zeros((2, 3, 4, 5)))
])
def test_check_image_shape(candidate):
    try:
        assert candidate._check_image_shape()
    except ValueError:
        with pytest.raises(ValueError):
            candidate._check_image_shape()


@pytest.mark.parametrize("candidate", [
    Processing(imread(dog_source, as_gray=False)),
    Processing(dog_image)
])
def test_check_grayscale(candidate):
    try:
        assert candidate._check_grayscale()
    except custom_errors.GrayscaleError:
        with pytest.raises(custom_errors.GrayscaleError):
            candidate._check_grayscale()
'''
