import pytest
from random import choice
from string import ascii_uppercase
from database import ImageProcessingDB


def random_id():
    return ''.join(choice(ascii_uppercase) for _ in range(10))


@pytest.fixture()
def database_obj():
    return ImageProcessingDB()


@pytest.fixture()
def image_info():
    image_i = {
        "image_id": "0",
        "image_data": "test",
        "height": 100,
        "width": 100,
        "format": "png",
        "processing_time": 30,
        "process": "hist_eq",
    }
    return image_i


def test_add_image(database_obj, image_info):
    user_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = random_id()
    image = database_obj.add_image(user_id, image_info)
    assert image["image_data"] == "test"


def test_add_image_with_parent(database_obj, image_info):
    user_id = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    image_1 = database_obj.find_image(parent_id, user_id)
    image_2 = database_obj.find_image(child_id, user_id)

    assert child_id in image_1.child_ids and \
        image_2.parent_id == parent_id and \
        image_1.process_history == [parent_id]


def test_add_image_no_image_id(database_obj, image_info):
    with pytest.raises(AttributeError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        del u_image["image_id"]
        database_obj.add_image(user_id, u_image)


def test_add_image_bad_image_id(database_obj, image_info):
    with pytest.raises(ValueError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["image_id"] = 1234123
        database_obj.add_image(user_id, u_image)


def test_add_image_bad_image(database_obj, image_info):
    with pytest.raises(TypeError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["image_data"] = 1234123
        database_obj.add_image(user_id, u_image)


def test_add_image_bad_dim(database_obj, image_info):
    with pytest.raises(TypeError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["image_id"] = random_id()
        u_image["width"] = "!23"
        database_obj.add_image(user_id, u_image)


@pytest.mark.parametrize("format", [
    "asdf", "blah"
])
def test_add_image_bad_format(database_obj, image_info, format):
    with pytest.raises(ValueError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["image_id"] = random_id()
        u_image["format"] = format
        database_obj.add_image(user_id, u_image)


def test_add_image_no_processing_time(database_obj, image_info):
    with pytest.raises(AttributeError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        del u_image["processing_time"]
        database_obj.add_image(user_id, u_image)


def test_add_image_bad_processing_time(database_obj, image_info):
    with pytest.raises(TypeError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["image_id"] = random_id()
        u_image["processing_time"] = 123.4
        database_obj.add_image(user_id, u_image)


@pytest.mark.parametrize("process", [
    "test", "HIST_EQ", "ram_lak"
])
def test_add_image_bad_process(database_obj, image_info, process):
    with pytest.raises(ValueError):
        user_id = random_id()
        u_image = image_info
        u_image["user_id"] = user_id
        u_image["process"] = process
        u_image["image_id"] = random_id()
        database_obj.add_image(user_id, u_image)


def test_add_user(database_obj):
    user_id = random_id()
    u = database_obj.add_user(user_id)
    assert u.user_id == user_id


def test_add_user_with_image(database_obj, image_info):
    user_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = random_id()
    database_obj.add_image(user_id, u_image)

    db_user = database_obj.find_user(user_id)
    assert db_user.user_id == user_id


def test_add_bad_user(database_obj, image_info):
    with pytest.raises(ValueError):
        user_id = random_id()
        database_obj.add_user(user_id)
        database_obj.add_user(user_id)


def test_update_user(database_obj):
    user_id = random_id()
    database_obj.update_process_history(user_id, ["ID1", "ID2"])

    db_user = database_obj.find_user(user_id)
    assert db_user.uploads["ID1"] == "ID2"


def test_remove_image(database_obj, image_info):
    user_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = random_id()
    database_obj.add_image(user_id, u_image)
    database_obj.remove_image(u_image["image_id"])
    image = database_obj.find_image(u_image["image_id"], user_id)
    assert image is None


def test_find_image(database_obj, image_info):
    user_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = random_id()
    database_obj.add_image(user_id, u_image)
    image = database_obj.find_image(u_image["image_id"], user_id)
    assert image.image_id == u_image["image_id"]


def test_find_image_child(database_obj, image_info):
    user_id = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    assert database_obj.find_image_child(
        parent_id, user_id) == [child_id]


def test_find_image_parent(database_obj, image_info):
    user_id = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["user_id"] = user_id
    u_image["image_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(user_id, u_image)

    parent_image = database_obj.find_image_parent(child_id, user_id)
    parent_image = database_obj.image_to_json(parent_image)
    assert parent_image["image_id"] == parent_id


def test_find_user(database_obj):
    user_id = random_id()
    database_obj.add_user(user_id)
    u = database_obj.find_user(user_id)
    assert u.user_id == user_id
