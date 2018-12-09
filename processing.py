import datetime
import skimage
import numpy as np
from skimage import exposure, util, filters, color
import matplotlib.pyplot as plt
from skimage.io import imread
import cv2
import os

# This converts 3D RBG to 2D grayscale
# image_gray = skimage.color.rgb2grey(self.image)
# This converts 3D RBG to 2D grayscale
# output_as_rgb = skimage.color.gray2rgb(img_array)


def output_to_rgb(img_array: np.array):
    output_as_rgb = skimage.color.gray2rgb(img_array)
    return output_as_rgb


def output_0_to_255_as_int(img_array: np.array):
    output_as_0_255 = exposure.rescale_intensity(
        img_array, out_range=(0, 255))
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
        image_rescale_output = output_0_to_255_as_int(output_to_rgb(image_rescale))
        return image_rescale_output, b.stop()

    def log_compression(self, base=10):
        """
        Performs log compression of self.image.
        Args:
            base: base of the log which is applied to the image
        Returns:
            Numpy.Array representation of log compressed image
        """
        b = Benchmark()

        if self._check_grayscale() == 'GRAY':
            image_log = np.log(self.image + 1) / np.log(base)
            image_log_output = output_0_to_255_as_int(output_to_rgb(image_log))
            return image_log_output, b.stop()
        if self._check_grayscale() == 'COLOR':
            # TODO: Haven't figured out how to log compress color images yet.
            '''
            img_yuv = cv2.cvtColor(self.image, cv2.COLOR_RGB2YUV)
            img_yuv[:, :, 0] = np.log(img_yuv[:, :, 0] + 1) / np.log(base)
            img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
            image_log_output = output_0_to_255_as_int(img_output)
            return image_log_output, b.stop()
            '''
            return self.image, b.stop()

    def reverse_video(self):
        """
        Inverts the black/white pixels of an image.
        Only works for grayscale images
        Returns:
            Numpy.Array representation of reversed image
        """
        # TODO: Please check inputs here!

        b = Benchmark()
        if self._check_grayscale() == 'GRAY':
            image_reverse = util.invert(self.image)
            image_reverse_output = output_0_to_255_as_int(output_to_rgb(image_reverse))
            return image_reverse_output, b.stop()
        if self._check_grayscale() == 'COLOR':
            raise ValueError("Can only use reverse video for grayscale images")

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
        unsharp_image = cv2.addWeighted(temp_self_image, 1.5, image_blur, -0.5, 0)
        image_sharpen_output = output_0_to_255_as_int(output_to_rgb(unsharp_image))
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
            plt.hist(image.ravel(), bins=256, range=(0.0, 1.0), color='black')
            plt.xlabel('Normalized Pixel Intensity')
            plt.ylabel('Number of Pixels')
            plt.xlim(0, 1)
            plt.ylim([0, 75000])
            plt.savefig("./temp.png")
            plt.close()
            hist_np_array = imread('temp.png')
            os.remove("temp.png")
            hist_np_array_output = output_0_to_255_as_int(output_to_rgb(hist_np_array))
            return hist_np_array_output
        if self._check_grayscale() == 'COLOR':
            color = ('r', 'g', 'b')
            for i, col in enumerate(color):
                histr = cv2.calcHist([image], [i], None, [256], [0, 255])
                plt.plot(histr, color=col)
                plt.xlabel('Pixel Intensity')
                plt.ylabel('Number of Pixels')
                plt.xlim([0, 256])
                plt.ylim([0, 75000])
                plt.savefig("./temp.png")
            plt.close()
            hist_np_array = imread('temp.png')
            # os.remove("temp.png")
            hist_np_array_output = output_0_to_255_as_int(output_to_rgb(hist_np_array))
            return hist_np_array_output

    def _check_image_type(self):
        """
        Checks if the input image is a numpy array.
        Returns:
            bool: If the image is valid.
        """
        # Image input should be an ARRAY.
        if type(self.image) != np.ndarray:
            raise TypeError("Image is not a numpy array")
        return True

    def _check_image_shape(self):
        """
        Checks if image numpy array has valid dimensions
        Returns:
            bool: If the image is valid.
        """
        # Image array should be grayscale or color (length = 2 or 3)
        if len(self.image.shape) != 2 and len(self.image.shape) != 3:
            raise ValueError("Dimensions of input array incorrect")
        return True

    def _check_grayscale(self):
        """
        Checks if the input image is grayscale.
        Returns:
            GRAY: If the image is grayscale
            COLOR: if the image is color
        """
        # Image array length should not be 3 (color).
        if len(self.image.shape) == 2:
            return 'GRAY'
        if len(self.image.shape) == 3:
            return 'COLOR'
