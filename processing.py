import io
import base64
import imageio
import numpy as np
import datetime
import matplotlib.pyplot as plt
from skimage import exposure, util, filters


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
        self.image = self.b64_to_numpy(image)

    def hist_eq(self):
        """
        Employs histogram equalization on given image.
        Args:
            image: Image to perform histogram equalization on.
        """
        b = Benchmark()
        image_he = exposure.equalize_hist(self.image)
        return self.numpy_to_b64(image_he), b.stop()

    def contrast_stretch(self, percentile=(10, 90)):
        """
        Employs contrast stretching on given image.
        Args:
            image: Image to perform contrast stretching on.
            percentile: percentile range of pixel intensity to stretch
        """
        b = Benchmark()
        p1, p2 = np.percentile(self.image, percentile)
        image_rescale = exposure.rescale_intensity(self.image, in_range=(p1, p2))
        return image_rescale, b.stop()

    def log_compression(self, base=10):
        """
        Performs log compression of the image.
        Args:
            base: base of the log which is applied to the image
        """
        b = Benchmark()
        image_log = np.log(self.image + 1) / np.log(base)
        return self.numpy_to_b64(image_log), b.stop()

    def reverse_video(self):
        """
        Creates a reverse video of given video (image/frame list).
        Args:
            image: Image to perform inversion on.
        """
        b = Benchmark()
        image_reverse = util.invert(self.image)
        return self.numpy_to_b64(image_reverse), b.stop()

    def blur(self, sigma=5):
        """
        Employs a blurring filter on given image.
        Args:
            image: Image to perform blurring on.
            sigma: Standard deviation for Gaussian blur kernel
        """
        b = Benchmark()
        image_blur = filters.gaussian(self.image, sigma)
        return self.numpy_to_b64(image_blur), b.stop()

    def sharpen(self, filter_type=None):
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
        b = Benchmark()
        image_blur = self.blur(self.image, 5)
        alpha = 1
        image_sharpened = self.image + alpha * (self.image - image_blur)
        return self.numpy_to_b64(image_sharpened), b.stop()

    def b64_to_numpy(self, img_bytes):
        """
        Converts bytes into numpy array.
        Args:
            img_bytes: Bytes of the image to convert.

        Returns:

        """
        if type(img_bytes) == np.ndarray:
            return img_bytes
        return imageio.imread(io.BytesIO(base64.b64decode(img_bytes)))

    def numpy_to_b64(self, img):
        """
        Converts numpy into bytes.
        Args:
            img: Image to convert.

        Returns:
            str: Base64 string.
        """
        return base64.b64encode(img)
