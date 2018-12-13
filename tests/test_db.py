import pytest
from random import choice
from string import ascii_uppercase
from database import ImageProcessingDB
from processing import Processing


def random_id():
    return ''.join(choice(ascii_uppercase) for _ in range(10))


@pytest.fixture()
def database_obj():
    return ImageProcessingDB()


@pytest.fixture()
def image_info():
    image_i = {
        "filename": "test_name",
        "image_id": "0",
        "image_data": "test",
        "height": 100,
        "width": 100,
        "format": "png",
        "processing_time": 30,
        "process": "hist_eq",
        "histogram": "test"
    }
    return image_i


def test_add_image(database_obj, image_info):
    email = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = random_id()
    image = database_obj.add_image(email, image_info)
    image = database_obj.image_to_json(image)
    assert image["image_data"] == "test"


def test_add_image_with_parent(database_obj, image_info):
    email = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = parent_id
    database_obj.add_image(email, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(email, u_image)

    image_1 = database_obj.find_image(parent_id, email)
    image_2 = database_obj.find_image(child_id, email)

    assert child_id in image_1.child_ids and \
           image_2.parent_id == parent_id and \
           image_1.process_history == [parent_id]


def test_add_image_no_image_id(database_obj, image_info):
    with pytest.raises(AttributeError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        del u_image["image_id"]
        database_obj.add_image(email, u_image)


def test_add_image_bad_image_id(database_obj, image_info):
    with pytest.raises(ValueError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["image_id"] = 1234123
        database_obj.add_image(email, u_image)


def test_add_image_bad_image(database_obj, image_info):
    with pytest.raises(TypeError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["image_data"] = 1234123
        database_obj.add_image(email, u_image)


def test_add_image_bad_dim(database_obj, image_info):
    with pytest.raises(TypeError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["image_id"] = random_id()
        u_image["width"] = "!23"
        database_obj.add_image(email, u_image)


@pytest.mark.parametrize("format", [
    "asdf", "blah"
])
def test_add_image_bad_format(database_obj, image_info, format):
    with pytest.raises(ValueError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["image_id"] = random_id()
        u_image["format"] = format
        database_obj.add_image(email, u_image)


def test_add_image_no_processing_time(database_obj, image_info):
    with pytest.raises(AttributeError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        del u_image["processing_time"]
        database_obj.add_image(email, u_image)


def test_add_image_bad_processing_time(database_obj, image_info):
    with pytest.raises(TypeError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["image_id"] = random_id()
        u_image["processing_time"] = 123.4
        database_obj.add_image(email, u_image)


@pytest.mark.parametrize("process", [
    "test", "HIST_EQ", "ram_lak"
])
def test_add_image_bad_process(database_obj, image_info, process):
    with pytest.raises(ValueError):
        email = random_id()
        u_image = image_info
        u_image["email"] = email
        u_image["process"] = process
        u_image["image_id"] = random_id()
        database_obj.add_image(email, u_image)


def test_add_user(database_obj):
    email = random_id()
    u = database_obj.add_user(email)
    assert u.email == email


def test_add_user_with_image(database_obj, image_info):
    email = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = random_id()
    database_obj.add_image(email, u_image)

    db_user = database_obj.find_user(email)
    assert db_user.email == email


def test_add_bad_user(database_obj, image_info):
    with pytest.raises(ValueError):
        email = random_id()
        database_obj.add_user(email)
        database_obj.add_user(email)


def test_update_user(database_obj):
    email = random_id()
    database_obj.update_process_history(email, ["ID1", "ID2"])

    db_user = database_obj.find_user(email)
    assert db_user.uploads["ID1"] == "ID2"


def test_update_user_process(database_obj):
    email = random_id()
    database_obj.add_user(email)
    database_obj.update_user_process(email, "hist_eq")
    db_user = database_obj.find_user(email)
    assert db_user.process_count["hist_eq"] == 1


def test_remove_image(database_obj, image_info):
    email = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = random_id()
    database_obj.add_image(email, u_image)
    database_obj.remove_image(u_image["image_id"])
    image = database_obj.find_image(u_image["image_id"], email)
    assert image is None


def test_find_image(database_obj, image_info):
    email = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = random_id()
    database_obj.add_image(email, u_image)
    image = database_obj.find_image(u_image["image_id"], email)
    assert image.image_id == u_image["image_id"]


def test_find_image_child(database_obj, image_info):
    email = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = parent_id
    database_obj.add_image(email, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(email, u_image)

    assert database_obj.find_image_child(
        parent_id, email) == [child_id]


def test_find_image_parent(database_obj, image_info):
    email = random_id()

    parent_id = random_id()
    u_image = image_info
    u_image["email"] = email
    u_image["image_id"] = parent_id
    database_obj.add_image(email, u_image)

    child_id = random_id()
    u_image = image_info
    u_image["image_id"] = child_id
    u_image["parent_id"] = parent_id
    database_obj.add_image(email, u_image)

    parent_image = database_obj.find_image_parent(child_id, email)
    parent_image = database_obj.image_to_json(parent_image)
    assert parent_image["image_id"] == parent_id


def test_find_user(database_obj):
    email = random_id()
    database_obj.add_user(email)
    u = database_obj.find_user(email)
    assert u.email == email
