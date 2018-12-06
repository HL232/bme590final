import numpy as np
from skimage import exposure
from skimage import util
from skimage import filters


class Processing(object):
    """
    Processing class contains all the methods needed to process the image.
    Any image passed into an instance of Processing must be an
    array-like object
    """
    def __init__(self):
        pass

    @staticmethod
    def hist_eq(image):
        """
        Employs histogram equalization on given image.
        Args:
            image: Image to perform histogram equalization on.
        """
        image_he = exposure.equalize_hist(image)
        return image_he

    @staticmethod
    def contrast_stretch(image, percentile=(10, 90)):
        """
        Employs contrast stretching on given image.
        Args:
            image: Image to perform contrast stretching on.
            percentile: percentile range of pixel intensity to stretch
        """
        p1, p2 = np.percentile(image, percentile)
        image_rescale = exposure.rescale_intensity(image, in_range=(p1, p2))
        return image_rescale

    @staticmethod
    def log_compression(image, base=10):
        """
        Performs log compression of the image.
        Args:
            image: Image to perform inversion on.
            base: base of the log which is applied to the image
        """
        image_log = np.log(image + 1) / np.log(base)
        return image_log

    @staticmethod
    def reverse_video(image):
        """
        Creates a reverse video of given video (image/frame list).
        Args:
            image: Image to perform inversion on.
        """
        image_reverse = util.invert(image)
        return image_reverse

    @staticmethod
    def blur(image, sigma=5):
        """
        Employs a blurring filter on given image.
        Args:
            image: Image to perform blurring on.
            sigma: Standard deviation for Gaussian blur kernel
        """
        image_blur = filters.gaussian(image, sigma)
        return image_blur

    def sharpen(self, image, filter_type=None):
        """
        Employs a sharpening filter on given image.
        Args:
            image: Image to perform sharpening on.
            filter_type: The type of the filter to use.
        """
        # image_sharpened = filters.unsharp_mask(image, radius=1, amount=1)
        # unsharp_mask but it doesn't seem to exist in
        # skimage.filters anymore
        # This is the mathematical method of sharpening:
        # sharp_image = original + alpha * (original - blurred)
        image_blur = self.blur(image, 5)
        alpha = 1
        image_sharpened = image + alpha * (image - image_blur)
        return image_sharpened

    def _check_valid_image(self, image):
        """
        Checks if the input image is valid to be processed.

        Returns:
            bool: If the image is valid.
        """
        # Image input should be an ARRAY.
        return True
