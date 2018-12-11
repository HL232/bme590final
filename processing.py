import datetime
import skimage
import numpy as np
from skimage import exposure, util, color
import matplotlib.pyplot as plt
import imageio
import cv2
import os

# OKAY SELF, HERE'S A NOTE SO YOU DON'T KEEP MAKING THE SAME MISTAKE
# if you get a singular line as an output of histogram()
# it's because all other processing functions output
# a tuple of form: array, time
# whereas histogram only outputs an array.
# just remove the [0] at the end of histogram to access
# the whole array


def output_to_rgb(img_array: np.array):
    """
    Converts the image array to RGB
    Args:
        img_array: A numpy array representing the image
    Returns:
        output_as_rgb: the image represented as a RGB image
    """
    output_as_rgb = skimage.color.gray2rgb(img_array)
    return output_as_rgb


def output_0_to_255_as_int(img_array: np.array):
    """
    Converts the image array integers in range 0-255
    Args:
        img_array: A numpy array representing the image
    Returns:
        output_as_in: the image array as integer 0-255
    """
    output_as_0_255 = exposure.rescale_intensity(
        img_array, out_range=(0, 255))
    output_as_int = output_as_0_255.astype(int)
    return output_as_int


def check_grayscale(image):
        """
        Checks if the input image is grayscale OUTSIDE Processing class.
        Returns:
            GRAY: If the image is grayscale
            COLOR: if the image is color
        """
        # Image array length should not be 3 (color).
        a = image[:, :, 0] == image[:, :, 1]
        b = image[:, :, 1] == image[:, :, 2]
        c = a == b
        if c.all():
            return 'GRAY'
        else:
            return 'COLOR'


class Benchmark(object):
    """
    Benchmark class used to document time it takes to process images
    """
    def __init__(self):
        """
        Initializes the benchmark class with the start time
        """
        self.start_time = datetime.datetime.now()

    def stop(self):
        """
        Determines the stop time of when the process finished
        Returns:
            Time in milliseconds the process ran for
        """
        delta = datetime.datetime.now() - self.start_time
        return int(delta.total_seconds() * 1000)  # milliseconds


class Processing(object):
    """
    Processing class contains all the methods needed to process the image.
    Any image passed into an instance of Processing must be an
    array-like object
    """

    def __init__(self, image):
        """
        Initializes the Processing class with an image.
        If the image is color, the array is unchanged
        If the image is grayscale, the image is converted to
        2D grayscale array
        """
        self._check_image_type(image)
        self._check_image_shape(image)
        if check_grayscale(image) == 'COLOR':
            self.image = image
        if check_grayscale(image) == 'GRAY':
            self.image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def hist_eq(self):
        """
        Employs histogram equalization on self.image.
        Returns:
            Numpy.Array representation of histogram equilization image
        """
        b = Benchmark()
        if self._check_grayscale() == 'GRAY':
            image_he = exposure.equalize_hist(self.image)
            image_he_output = output_0_to_255_as_int(output_to_rgb(image_he))
            return image_he_output, b.stop()
        if self._check_grayscale() == 'COLOR':
            # This method of histogram equalization for color images
            # equilizes the Y channel of RBG converted to YUV images
            # YUV is equivalent to YCbCr in our case
            yuv_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2YUV)
            yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])
            img_output = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2RGB)
            return img_output, b.stop()

    def contrast_stretch(self, percentile=(10, 90)):
        """
        Employs contrast stretching on self.image.
        Args:
            percentile: percentile range of pixel intensity to stretch
        Returns:
            Numpy.Array representation of contrast stretched image
        """
        # This same method should work for both color and grayscale images
        b = Benchmark()
        p1, p2 = np.percentile(self.image, percentile)
        image_rescale = exposure.rescale_intensity(
            self.image, in_range=(p1, p2))
        image_rescale_output = output_0_to_255_as_int(
            output_to_rgb(image_rescale))
        return image_rescale_output, b.stop()

    def log_compression(self):
        """
        Performs log compression of self.image.
        Args:
            base: base of the log which is applied to the image
        Returns:
            Numpy.Array representation of log compressed image
        """
        b = Benchmark()

        if self._check_grayscale() == 'GRAY':
            # IS THIS WORKING???**********************************
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
            image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
            image_hsv[:, :, 1] = np.log(image_hsv[:, :, 1] + 1)
            image_output = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
            image_log_output = output_0_to_255_as_int(image_output)
            return image_log_output, b.stop()
        if self._check_grayscale() == 'COLOR':
            image_hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
            image_hsv[:, :, 0] = np.log(image_hsv[:, :, 0] + 1)
            image_output = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
            image_log_output = output_0_to_255_as_int(image_output)
            return image_log_output, b.stop()

    def reverse_video(self):
        """
        Inverts the black/white pixels of an image.
        Only works for grayscale images
        Returns:
            Numpy.Array representation of reversed image
            ValueError if the user inputs a color image
        """
        b = Benchmark()
        if self._check_grayscale() == 'GRAY':
            image_reverse = util.invert(self.image)
            image_reverse_output = output_0_to_255_as_int(
                output_to_rgb(image_reverse))
            return image_reverse_output, b.stop()
        if self._check_grayscale() == 'COLOR':
            raise ValueError("reverse video only for grayscale images")

    def blur(self):
        """
        Employs a Gaussian blurring filter on given image.
        Returns:
            Numpy.Array representation of blurred image
        """
        # Blur should be the same for grayscale and color images
        b = Benchmark()
        image_blur = cv2.GaussianBlur(self.image, (19, 19), 10)
        image_blur_output = output_0_to_255_as_int(output_to_rgb(image_blur))
        return image_blur_output, b.stop()

    def sharpen(self):
        """
        Employs a sharpening filter on given image.
        Returns:
            Numpy.Array representation of sharpened image
        """
        # Sharpen should be the same for grayscale and color images
        b = Benchmark()
        temp_self_image = self.image
        image_blur = cv2.GaussianBlur(temp_self_image, (19, 19), 10)
        unsharp_image = cv2.addWeighted(
            temp_self_image, 1.5, image_blur, -0.5, 0)
        image_sharpen_output = output_0_to_255_as_int(
            output_to_rgb(unsharp_image))
        return image_sharpen_output, b.stop()

    def histogram(self, image):
        """
        Returns a histogram of the image
        Args:
            image: Image to find histogram of
        Returns:
            Numpy.Array representation of histogram of image
        """
        if self._check_grayscale() == 'GRAY':
            histr = plt.hist(image.ravel(), 256, [0, 256], color='black')
            plt.xlabel('Pixel Intensity')
            plt.ylabel('Number of Pixels')
            plt.xlim(-10, 270)
            plt.ylim([0, max(histr[0])+5000])
            plt.savefig("./temp.png")
            plt.close()
            hist_np_array = imageio.imread('temp.png')
            os.remove("temp.png")
            hist_np_array_output = output_0_to_255_as_int(
                output_to_rgb(hist_np_array))
            return hist_np_array_output
        if self._check_grayscale() == 'COLOR':
            image = np.uint8(image)
            color = ('r', 'g', 'b')
            max_pixel = 0
            for i, col in enumerate(color):
                histr = cv2.calcHist([image], [i], None, [256], [0, 255])
                plt.plot(histr, color=col)
                if max(histr) > max_pixel:
                    max_pixel = max(histr)
            plt.xlabel('Pixel Intensity')
            plt.ylabel('Number of Pixels')
            plt.xlim([-10, 270])
            plt.ylim([0, max(max_pixel)+5000])
            plt.savefig("./temp.png")
            plt.close()
            hist_np_array = imageio.imread('temp.png')
            os.remove("temp.png")
            hist_np_array_output = output_0_to_255_as_int(
                output_to_rgb(hist_np_array))
            return hist_np_array_output

    def _check_image_type(self, image):
        """
        Checks if the input image is a numpy array.
        Returns:
            bool: If the image is valid.
        """
        if type(image) != imageio.core.util.Array:
            raise TypeError("Image is not a imageio Array")
        return True

    def _check_image_shape(self, image):
        """
        Checks if image numpy array has valid dimensions
        Returns:
            bool: If the image is valid.
        """
        if len(image.shape) != 2 and len(image.shape) != 3:
            raise ValueError("Dimensions of input array incorrect")
        return True

    def _check_grayscale(self):
        """
        Checks if the input image is grayscale WITHIN Processing class.
        Returns:
            GRAY: If the image is grayscale
            COLOR: if the image is color
        """
        if len(self.image.shape) == 2:
            return 'GRAY'
        if len(self.image.shape) == 3:
            return 'COLOR'
