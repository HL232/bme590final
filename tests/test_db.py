import pytest
import base64
from random import choice
from string import ascii_uppercase
from database import ImageProcessingDB


def random_id():
    return ''.join(choice(ascii_uppercase) for _ in range(10))


@pytest.fixture()
def database_obj():
    return ImageProcessingDB()


@pytest.fixture()
def image_info_test():
    image_info = {
        "image_id": random_id(),
        "image": base64.encode("test"),
        "height": 100,
        "width": 100,
        "format": "png",
        "processing_time": 30,
        "process": "hist_eq",
    }
    return image_info


def test_add_image(database_obj):
    pass


def test_add_image_with_parent(database_obj):
    pass


def test_add_image_bad_image_id(database_obj):
    pass


def test_add_image_bad_image(database_obj):
    pass


def test_add_image_bad_dim(database_obj):
    pass


def test_add_image_bad_format(database_obj):
    pass


def test_add_image_bad_processing_time(database_obj):
    pass


def test_add_image_bad_process(database_obj):
    pass


def test_add_user(database_obj):
    pass


def test_add_user_with_image(database_obj):
    pass


def test_add_bad_user(database_obj):
    pass


def test_update_user_uploads(database_obj):
    pass


def test_update_description(database_obj):
    pass


def test_remove_image(database_obj):
    pass


def test_find_image(database_obj):
    pass


def test_find_image_child(database_obj):
    pass


def test_find_image_parent(database_obj):
    pass


def test_find_user(database_obj):
    pass
