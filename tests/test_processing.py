import pytest
from processing import *
import numpy as np
import imageio
from time import sleep


dog_source = 'https://thumbs.dreamstime.com/b' \
             '/grayscale-photography-short-coated-dog-83077538.jpg'
dog_gray = imageio.imread(dog_source, format="JPG")

dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
          'sites/default/files/legacy/images/' \
          'resource-centre/IFAW%20Northern%20Dog.JPG'
dog_color = imageio.imread(dog_source, format="JPG")


def test_output_to_rgb():
    a = imageio.core.util.Array(np.zeros((2, 3)))
    assert np.array_equal(output_to_rgb(a), np.zeros((2, 3, 3)))


def test_output_0_to_255_as_int():
    a = np.array(
        [[[0.,  1.],
            [0.,  0.],
            [0.5,  0.]],
            [[.2,  0.],
             [0.,  0.7],
             [1.,  0.]]])
    b = np.array(
        [[[0, 255],
          [0, 0],
          [127, 0]],
         [[51, 0],
          [0, 178],
          [255, 0]]])
    assert np.array_equal(output_0_to_255_as_int(a), b)


def test_stop():
    b = Benchmark()
    sleep(0.1)
    stop_time = b.stop()
    assert 100 <= stop_time < 120


# def test_hist_eq():



@pytest.mark.parametrize("candidate, expected", [
    (dog_gray, 'GRAY'),
    (dog_color, 'COLOR')
])
def test_check_grayscale(candidate, expected):
    assert check_grayscale(candidate) == expected


@pytest.mark.parametrize("candidate", [
    'blah',                                               
    3,
    2.4,
    [1, 2, 3],
    (1, 3),
    np.array([2, 3, 1, 0]),
    imageio.core.util.Array(np.array([2, 3, 1, 0]))
])
def test_check_image_type(candidate):
    p = Processing(dog_gray)
    try:
        assert p._check_image_type(candidate)
    except TypeError:
        with pytest.raises(TypeError):
            p._check_image_type(candidate)


@pytest.mark.parametrize("candidate", [
    imageio.core.util.Array(np.array([2, 3, 1, 0])),
    imageio.core.util.Array(np.zeros((2, 3))),
    imageio.core.util.Array(np.zeros((2, 3, 4))),
    imageio.core.util.Array(np.zeros((2, 3, 4, 5)))
])
def test_check_image_shape(candidate):
    p = Processing(dog_gray)
    try:
        assert p._check_image_shape(candidate)
    except ValueError:
        with pytest.raises(ValueError):
            p._check_image_shape(candidate)


@pytest.mark.parametrize("candidate, expected", [
    (Processing(dog_gray), 'GRAY'),
    (Processing(dog_color), 'COLOR')
])
def test__check_grayscale(candidate, expected):
        assert candidate._check_grayscale() == expected
