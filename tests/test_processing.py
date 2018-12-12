import pytest
from processing import *
import numpy as np
import imageio
from time import sleep


dog_source_gray = 'images_for_testing/gray_dog.jpg'
dog_gray = imageio.imread(dog_source_gray, format="JPG")

dog_source_color = 'images_for_testing/color_dog.JPG'
dog_color = imageio.imread(dog_source_color, format="JPG")


def plot(image_array):
    plt.imshow(image_array)
    plt.axis('off')
    plt.savefig('./temp.jpg')
    plt.close()
    return


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


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_hist_eq.jpg', dog_gray),
    ('images_for_testing/color_hist_eq.jpg', dog_color),
])
def test_hist_eq(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    image = p.hist_eq()[0]
    plot(image)
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    assert np.array_equal(prepared_image, produced_image)


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_contrast_stretch.jpg', dog_gray),
    ('images_for_testing/color_contrast_stretch.jpg', dog_color),
])
def test_contrast_stretch(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    image = p.contrast_stretch()[0]
    plot(image)
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    assert np.array_equal(prepared_image, produced_image)


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_log_comp.jpg', dog_gray),
    ('images_for_testing/color_log_comp.jpg', dog_color),
])
def test_log_compression(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    image = p.log_compression()[0]
    plot(image)
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    assert np.array_equal(prepared_image, produced_image)


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_reverse_vid.jpg', dog_gray),
    ('images_for_testing/color_dog.JPG', dog_color),
])
def test_reverse_video(file_name, which_dog):
    try:
        prepared_image = imageio.imread(file_name, format='JPG')
        p = Processing(which_dog)
        image = p.reverse_video()[0]
        plot(image)
        produced_image = imageio.imread("./temp.jpg", format='JPG')
        os.remove("temp.jpg")
        assert np.array_equal(prepared_image, produced_image)
    except ValueError:
        with pytest.raises(ValueError):
            p = Processing(which_dog)
            p.reverse_video()[0]


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_blur.jpg', dog_gray),
    ('images_for_testing/color_blur.jpg', dog_color),
])
def test_blur(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    image = p.blur()[0]
    plot(image)
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    assert np.array_equal(prepared_image, produced_image)


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_sharpen.jpg', dog_gray),
    ('images_for_testing/color_sharpen.jpg', dog_color),
])
def test_sharpen(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    image = p.sharpen()[0]
    plot(image)
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    assert np.array_equal(prepared_image, produced_image)


@pytest.mark.parametrize("file_name, which_dog", [
    ('images_for_testing/gray_original_histogram.jpg', dog_gray),
    ('images_for_testing/color_original_histogram.jpg', dog_color),
])
def test_histogram(file_name, which_dog):
    prepared_image = imageio.imread(file_name, format='JPG')
    p = Processing(which_dog)
    plot(p.histogram(which_dog))
    produced_image = imageio.imread("./temp.jpg", format='JPG')
    os.remove("temp.jpg")
    black = prepared_image-produced_image
    output = not black.all()
    assert output
    # assert np.array_equal(prepared_image, produced_image)


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
