import datetime
import skimage
import numpy as np
from skimage import exposure, util, filters
import custom_errors
import matplotlib.pyplot as plt
from skimage.io import imread


def output_0_to_255_as_int(img_array: np.array):
    output_as_rgb = skimage.color.gray2rgb(img_array)
    output_as_0_255 = exposure.rescale_intensity(
        output_as_rgb, out_range=(0, 255))
    output_as_int = output_as_0_255.astype(int)
    return output_as_int


class Benchmark(object):
    def __init__(self):
        self.start_time = datetime.datetime.now()

    def stop(self):
        delta = datetime.datetime.now() - self.start_time
        return int(delta.total_seconds() * 1000)  # milliseconds


class Processing(object):
    """
    Processing class contains all the methods needed to process the image.
    Any image passed into an instance of Processing must be an
    array-like object
    """

    def __init__(self, image):
        self.image = image

    def hist_eq(self):
        """
        Employs histogram equalization on given image.
        Args:
            image: Image to perform histogram equalization on.
        Returns:
            Numpy.Array representation of histogram equilization image
        """
        b = Benchmark()
        image_he = exposure.equalize_hist(self.image)
        image_he_output = output_0_to_255_as_int(image_he)
        return image_he_output, b.stop()

    def contrast_stretch(self, percentile=(10, 90)):
        """
        Employs contrast stretching on given image.
        Args:
            image: Image to perform contrast stretching on.
            percentile: percentile range of pixel intensity to stretch
        Returns:
            Numpy.Array representation of contrast stretched image
        """
        b = Benchmark()
        p1, p2 = np.percentile(self.image, percentile)
        image_rescale = exposure.rescale_intensity(
            self.image, in_range=(p1, p2))
        image_rescale_output = output_0_to_255_as_int(image_rescale)
        return image_rescale_output, b.stop()

    def log_compression(self, base=10):
        """
        Performs log compression of the image.
        Args:
            image: Image to perform inversion on.
            base: base of the log which is applied to the image
        Returns:
            Numpy.Array representation of log compressed image
        """
        b = Benchmark()
        if len(self.image.shape) == 3 and self.image.shape[2] != 3:
            image_gray = skimage.color.rgb2grey(self.image)
        else:
            image_gray = self.image
        image_log = np.log(image_gray + 1) / np.log(base)
        image_log_output = output_0_to_255_as_int(image_log)
        return image_log_output, b.stop()

    def reverse_video(self):
        """
        Creates a reverse video of given video (image/frame list).
        Only works for grayscale images
        Args:
            image: Image to perform inversion on.
        Returns:
            Numpy.Array representation of reversed image
        """
        # TODO: Please check inputs here!

        b = Benchmark()
        image_reverse = util.invert(self.image)
        image_reverse_output = output_0_to_255_as_int(image_reverse)
        return image_reverse_output, b.stop()

    def blur(self, sigma=5):
        """
        Employs a blurring filter on given image.
        Args:
            image: Image to perform blurring on.
            sigma: Standard deviation for Gaussian blur kernel
        Returns:
            Numpy.Array representation of blurred image
        """
        b = Benchmark()
        image_blur = filters.gaussian(self.image, sigma,
                                      preserve_range=True)
        image_blur_output = output_0_to_255_as_int(image_blur)
        return image_blur_output, b.stop()

    def sharpen(self):
        """
        Employs a sharpening filter on given image.
        Args:
            image: Image to perform sharpening on.
            filter_type: The type of the filter to use.
        Returns:
            Numpy.Array representation of sharpened image
        """
        # image_sharpened = filters.unsharp_mask(image, radius=1, amount=1)
        # unsharp_mask but it doesn't seem to exist in
        # skimage.filters anymore
        # This is the mathematical method of sharpening:
        # sharp_image = original + alpha * (original - blurred)
        b = Benchmark()
        image_blur = Processing(self.image).blur(5)[0]
        rbg_original_image = output_0_to_255_as_int(self.image)
        alpha = 1
        image_sharpened = rbg_original_image + \
            alpha * (rbg_original_image - image_blur)
        image_sharpened_output = output_0_to_255_as_int(image_sharpened)
        return image_sharpened_output, b.stop()

    def histogram_gray(self):
        """
        Returns a histogram of the image
        Args:
            image: Image to find histogram of
        Returns:
            Numpy.Array representation of histogram of image
        """
        plt.hist(self.image.ravel(), bins=256, range=(0.0, 1.0), color='black')
        plt.xlabel('Normalized Pixel Intensity')
        plt.ylabel('Number of Pixels')
        plt.xlim(0, 1)
        plt.savefig("./temp.png")
        plt.close()

        # this is a very crude method returning a numpy array
        hist_np_array = imread('temp.png')
        hist_np_array_output = output_0_to_255_as_int(hist_np_array)
        return hist_np_array_output

    def _check_image_type(self):
        """
        Checks if the input image is valid to be processed.
        Returns:
            bool: If the image is valid.
        """
        # Image input should be an ARRAY.
        if type(self.image) != np.ndarray:
            raise TypeError("Image is not a numpy array")
        return True

    def _check_image_shape(self):
        # Image array should be grayscale or color (length = 2 or 3)
        if len(self.image.shape) != 2 and len(self.image.shape) != 3:
            raise ValueError("Dimensions of input array incorrect")
        return True

    def _check_grayscale(self):
        """
        Checks if the input image is grayscale.
        Returns:
            bool: True if the image is grayscale.
        """
        # Image array length should not be 3 (color).
        if len(self.image.shape) == 3:
            raise custom_errors.GrayscaleError("Image is a color image")
        return True
