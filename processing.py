import skimage
import matplotlib.pyplot as plt


class Processing(object):
    def __init__(self):
        pass

    def hist_eq(self, image):
        """
        Employs histogram equalization on given image.
        Args:
            image: Image to perform histogram equalization on.
        """
        pass

    def contrast_stretch(self, image):
        """
        Employs contrast stretching on given image.
        Args:
            image: Image to perform contrast stretching on.
        """
        pass

    def reverse_video(self, video):
        """
        Creates a reverse video of given video (image/frame list).
        Args:
            image: Image to perform contrast stretching on.
        """
        pass

    def sharpen(self, image, filter_type=None):
        """
        Employs a sharpening filter on given image.
        Args:
            image: Image to perform sharpening on.
            filter_type: The type of the filter to use.
        """
        pass

    def blur(self, image, radius=5):
        """
        Employs a blurring filter on given image.
        Args:
            image: Image to perform blurring on.
            radius: Radius of the Gaussian blur.
        """
        pass

    def _check_valid_image(self, image):
        """
        Checks if the input image is valid to be processed.

        Returns:
            bool: If the image is valid.
        """
        return True
