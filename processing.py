import datetime
import skimage
import numpy as np
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
        self.image = image

    def hist_eq(self):
        """
        Employs histogram equalization on given image.
        Args:
            image: Image to perform histogram equalization on.
        """
        # TODO: Make sure you raise exceptions if not grayscale/
        # convert to grayscale for them.
        b = Benchmark()
        image_he = exposure.equalize_hist(self.image)
        image_he = exposure.rescale_intensity(image_he,
                                              out_range=(0, 255))
        return image_he, b.stop()

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
        if len(self.image.shape) == 3 and self.image.shape[2] != 3:
            image_gray = skimage.color.rgb2grey(self.image)
        else:
            image_gray = self.image
        image_log = np.log(image_gray + 1) / np.log(base)
        rgb_image_log = skimage.color.gray2rgb(image_log)
        # print(rgb_image_log.shape, rgb_image_log[0][0])
        return rgb_image_log.astype(int), b.stop()

    def reverse_video(self):
        """
        Creates a reverse video of given video (image/frame list).
        Args:
            image: Image to perform inversion on.
        """
        # TODO: Please check inputs here!

        b = Benchmark()
        image_reverse = util.invert(self.image)
        return image_reverse, b.stop()

    def blur(self, sigma=5):
        """
        Employs a blurring filter on given image.
        Args:
            image: Image to perform blurring on.
            sigma: Standard deviation for Gaussian blur kernel
        """
        b = Benchmark()
        image_blur = filters.gaussian(self.image, sigma,
                                      preserve_range=True)
        return image_blur.astype(int), b.stop()

    def sharpen(self):
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
        image_blur = Processing(self.image).blur(5)[0]
        alpha = 1
        image_sharpened = self.image + alpha * (self.image - image_blur)
        return image_sharpened, b.stop()
