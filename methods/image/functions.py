from PIL.Image import Image
from numpy import asarray, ndarray


def calculate_averages(image: Image, /) -> tuple[ndarray, ndarray]:
    """
    Takes an image, converts it to grayscale and returns average values for every row and column.
    """
    a = asarray(image.convert('L'), int)
    return a.mean(0, int), a.mean(1, int)


def calculate_difference(im1: Image, im2: Image, /) -> tuple[ndarray, ndarray]:
    """
    Takes two images, converts them to grayscale and returns absolute difference between
    their average values for every row and column.
    """
    x1, y1 = calculate_averages(im1)
    x2, y2 = calculate_averages(im2)
    return abs(x1 - x2), abs(y1 - y2)


__all__ = 'calculate_averages', 'calculate_difference'
