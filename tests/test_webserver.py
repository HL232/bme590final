import io
import cv2
import base64
import pytest
import zipfile
import imageio
import skimage
import numpy as np
from flask import Flask
from random import choice
from string import ascii_uppercase

from database import ImageProcessingDB
from img_processor_web_server import get_app

app_name = "image_processor"
app = Flask(app_name)

# testing using DM
db = ImageProcessingDB()


def random_id():
    return ''.join(choice(ascii_uppercase) for _ in range(10))


def zip_to_b64(filepath):
    """
    Takes a zip file and turns it to base 64.
    Args:
        filepath: Filepath of the folder to zip

    Returns:
        str: base 64 representation of zip folder.
    """

    # convert zip file to base64
    with open(filepath, "rb") as f:
        bytes = f.read()
        base64_bytes = base64.b64encode(bytes)
        base64_string = base64_bytes.decode('utf-8')  # convert to string
        return base64_string


@pytest.fixture()
def flask_app():
    app = get_app()
    return app


@pytest.fixture()
def image_post():
    dog_source = "https://i.imgur.com/B15ubOP.jpg"
    dog_image = imageio.imread(dog_source)
    image_data = numpy_to_b64str(dog_image)
    image = {
        "filename": "test_name.jpg",
        "email": "",
        "image_id": "0",
        "image_data": image_data,
        "height": 100,
        "width": 100,
        "format": "jpg",
        "processing_time": 30,
        "process": "hist_eq",
        "histogram": "test"
    }
    return image


@pytest.fixture()
def image_post_png():
    dog_source = 'https://i.imgur.com/2Tqty1A.png'
    dog_image = imageio.imread(dog_source)
    image_data = numpy_to_b64str(dog_image)
    image = {
        "filename": "test_name.jpg",
        "email": "",
        "image_id": "0",
        "image_data": image_data,
        "height": 100,
        "width": 100,
        "format": "jpg",
        "processing_time": 30,
        "process": "hist_eq",
        "histogram": "test"
    }
    return image


@pytest.fixture()
def image_upload():
    dog_source = "https://i.imgur.com/B15ubOP.jpg"
    dog_image = imageio.imread(dog_source)
    image_data = numpy_to_b64str(dog_image)
    image = {
        "filename": "test_name.jpg",
        "email": "",
        "image_data": image_data,
    }
    return image


def b64str_to_numpy(b64_img):
    """
    Converts a b64str to numpy. Strips headers.
    Args:
        b64_img (str): base 64 representation of an image.

    Returns:
        np.ndarray: numpy array of image.

    """
    split = b64_img.split("base64,")  # get rid of header
    if len(split) == 2:
        b64_img = split[1]
    else:
        b64_img = split[0]
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    np_img = imageio.imread(image_buf, format="JPG")
    return np_img


def numpy_to_b64str(img):
    """
    Converts a numpy array into a base 64 string
    Args:
        img (np.array):

    Returns:
        str: base 64 representation of the numpy array/image.

    """
    img = img[..., ::-1]  # flip for cv conversion
    _, img = cv2.imencode('.jpg', img)  # strips header
    image_base64 = base64.b64encode(img)
    base64_string = image_base64.decode('utf-8')  # convert to string
    return base64_string


# --------------------------- tests begin --------------------------

# ----------------- Post tests ------------------------------

def test_post_upload_image_dict(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    resp = client.post('/api/process/upload_image', json=image_upload)
    image = resp.json
    db_image = b64str_to_numpy(image["image_data"])
    user = db.find_user(image["email"])
    assert _check_image(db_image) and \
           user.current_image == image["image_id"]


def test_post_upload_image_list(flask_app, image_upload):
    client = flask_app.test_client()
    image_uploads = []
    for i in range(3):
        image_upload["email"] = random_id()
        image_uploads.append(image_upload)
    resp = client.post('/api/process/upload_image', json=image_upload)
    image = resp.json
    db_image = b64str_to_numpy(image["image_data"])
    user = db.find_user(image["email"])
    assert _check_image(db_image) and \
           user.current_image == image["image_id"]


def test_post_upload_image_dict_list(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    image_uploads = {}
    filenames = []
    image_data = []
    for i in range(3):
        filenames.append("{}.jpg".format(random_id()))
        image_data.append(image_upload["image_data"])

    image_uploads["email"] = image_upload["email"]
    image_uploads["image_data"] = image_data
    image_uploads["filename"] = filenames

    resp = client.post('/api/process/upload_image', json=image_uploads)
    print(resp, resp.json)
    image = resp.json
    db_image = b64str_to_numpy(image["image_data"])
    user = db.find_user(image["email"])
    assert _check_image(db_image) and \
           user.current_image == image["image_id"]


def test_post_upload_image_zip_file(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    image_upload["filename"] = "test_folder.zip"
    image_upload["image_data"] = zip_to_b64(
        "tests/images_for_testing/test_folder.zip")
    resp = client.post('/api/process/upload_image', json=image_upload)
    image = resp.json
    db_image = b64str_to_numpy(image["image_data"])
    user = db.find_user(image["email"])
    assert _check_image(db_image) and \
           user.current_image == image["image_id"]


def test_post_upload_image_no_email(flask_app, image_upload):
    client = flask_app.test_client()
    del image_upload["email"]
    resp = client.post('/api/process/upload_image', json=image_upload)
    assert resp.json["error_type"] == "AttributeError"


def test_post_upload_image_no_filename(flask_app, image_upload):
    test = image_upload
    client = flask_app.test_client()
    del test["filename"]
    resp = client.post('/api/process/upload_image', json=image_upload)
    assert resp.json["error_type"] == "AttributeError"


@pytest.mark.parametrize("filename", [
    "test1.svg", "test", "blah.p"])
def test_post_upload_image_bad_filenames(
        flask_app, image_upload, filename):
    client = flask_app.test_client()
    image_upload["filename"] = filename
    resp = client.post('/api/process/upload_image', json=image_upload)
    assert resp.json["error_type"] == "TypeError"


def test_post_upload_image_no_image_data(flask_app, image_upload):
    client = flask_app.test_client()
    del image_upload["image_data"]
    resp = client.post('/api/process/upload_image', json=image_upload)
    assert resp.json["error_type"] == "AttributeError"


def test_post_change_image(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/upload_image', json=image_upload)
    client.post('/api/process/upload_image', json=image_upload)
    payload = {
        "email": image_upload["email"],
        "image_id": resp.json["image_id"]
    }
    client.post('/api/process/change_image', json=payload)

    image = resp.json[0]
    db_image = b64str_to_numpy(image["image_data"])
    user = db.find_user(image["email"])
    assert _check_image(db_image) and \
           user.current_image == image["image_id"]


def test_post_change_image_bad_id(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    resp = client.post('/api/process/upload_image', json=image_upload)
    print(resp, type(resp.json))
    payload = {
        "email": image_upload["email"],
        "image_id": "1"
    }
    resp = client.post('/api/process/change_image', json=payload)
    print(resp, type(resp.json))
    assert resp.json["error_type"] == "ValueError"


def test_post_change_image_no_id(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    payload = {
        "email": image_upload["email"]
    }
    resp = client.post('/api/process/change_image', json=payload)
    print(resp, type(resp.json))
    assert resp.json["error_type"] == "AttributeError"


@pytest.mark.parametrize("remove_key", [
    "email", "image_data", "child_ids"])
def test_post_bad_confirm_image(flask_app, image_upload, remove_key):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    resp = client.post('/api/process/upload_image', json=image_upload)
    print(resp)
    payload = resp.json
    del payload[remove_key]
    resp = client.post('/api/process/confirm', json=payload)
    assert resp.json["error_type"] == "AttributeError"


def test_post_hist_eq(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/hist_eq',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["hist_eq"] == 1


def test_post_image_contrast_stretch(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/contrast_stretch',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["contrast_stretch"] == 1


def test_post_image_log_compression(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/log_compression',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["log_compression"] == 1


def test_post_image_reverse_video_color(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    resp = client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/reverse_video',
                       json={"email": image_upload["email"]})
    assert resp.json["error_type"] == "ValueError"


def test_post_image_reverse_video(flask_app, image_upload):
    rev_upload = image_upload
    test_image = imageio.imread(
        "images_for_testing/gray_dog.jpg", format="JPG")
    rev_upload["image_data"] = numpy_to_b64str(test_image)

    client = flask_app.test_client()
    image_upload["email"] = random_id()
    upload_resp = client.post(
        '/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/reverse_video',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["reverse_video"] == 1


def test_post_image_sharpen(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/sharpen',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["sharpen"] == 1


def test_post_image_blur(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/blur',
                       json={"email": image_upload["email"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    assert _check_image(db_image) and \
           user.process_count["blur"] == 1


def test_post_email_image(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = "dukebme590.imageprocessor@gmail.com"
    resp = client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/email_image', json=image_upload)


def test_post_confirm(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["email"] = random_id()
    client.post('/api/process/upload_image',
                json=image_upload)
    resp = client.post('/api/process/blur',
                       json={"email": image_upload["email"]})
    resp = client.post('/api/process/confirm',
                       json=resp.json)

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(resp.json["email"])
    assert _check_image(db_image) and \
           user.current_image == resp.json["image_id"]


# ---------------- get tests ------------------------------

def test_get_current_image(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    resp = client.get('/api/image/get_current_image/{}'.format(email))

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["email"])
    current_id = user.current_image

    assert _check_image(db_image) and \
           current_id == resp.json["image_id"]


def test_get_previous_image(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    original = client.post('/api/process/upload_image', json=image_upload)
    original = original.json[0]

    resp = client.post('/api/process/blur', json={"email": email})
    client.post('/api/process/confirm', json=resp.json)

    # should set back to uploaded image
    resp = client.get('/api/image/get_previous_image/{}'.format(email))
    prev_image = resp.json

    user = db.find_user(email)
    curr_image = user.current_image

    assert prev_image["image_id"] == original["image_id"] \
           and curr_image == prev_image["image_id"]


def test_get_next_image(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    original = resp.json

    resp = client.post('/api/process/blur', json={"email": email})
    resp = client.post('/api/process/confirm', json=resp.json)
    blurred_image = resp.json
    resp = client.get('/api/image/get_previous_image/{}'.format(
        image_upload["email"]))
    previous_image = resp.json

    resp = client.get('/api/image/get_next_image/{}'.format(
        previous_image["email"]))
    next_image = resp.json

    user = db.find_user(image_upload["email"])
    current_id = user.current_image

    assert original["image_id"] == previous_image["image_id"] \
           and next_image["image_id"] == blurred_image["image_id"] \
           and current_id == blurred_image["image_id"]


# -------------------- test get user stuff ---------------------

def test_get_user(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    image_id = resp.json["image_id"]

    resp = client.get('/api/user/get_user/{}'.format(email))
    user = resp.json
    print(user)
    assert image_id in user["uploads"].keys() and \
           email == user["email"]


def test_get_user_no_email(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    del image_upload["email"]
    resp = client.post('/api/process/upload_image', json=image_upload)
    assert resp.json["error_type"] == "AttributeError"


def test_get_original_upload_ids(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    original_id = resp.json["image_id"]
    resp = client.post('/api/process/blur', json={"email": email})
    client.post('/api/process/confirm', json=resp.json)
    blurred_id = resp.json["image_id"]
    resp = client.get(
        '/api/user/get_original_upload_ids/{}'.format(email))
    ids = resp.json
    assert original_id in ids


def test_get_updated_upload_ids(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    print(resp.json)
    original_id = resp.json["image_id"]
    resp = client.post('/api/process/blur', json={"email": email})
    client.post('/api/process/confirm', json=resp.json)
    blurred_id = resp.json["image_id"]
    resp = client.get(
        '/api/user/get_updated_upload_ids/{}'.format(email))
    ids = resp.json
    assert blurred_id in ids


def test_get_upload_filenames(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    print(resp.json)
    resp = client.get(
        '/api/user/get_upload_filenames/{}'.format(email))
    names = resp.json  # should be a dict

    all_names = []
    for image_id in names.keys():
        all_names.append(names[image_id])
    assert image_upload["filename"] in all_names


def test_get_original_uploads(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    original_id = resp.json["image_id"]

    resp = client.post('/api/process/blur', json={"email": email})
    client.post('/api/process/confirm', json=resp.json)

    blurred_id = resp.json["image_id"]
    resp = client.get(
        '/api/user/get_original_uploads/{}'.format(email))
    images = resp.json

    assert len(images) == 1 and images[0]["image_id"] == original_id


def test_get_updated_uploads(flask_app, image_upload):
    client = flask_app.test_client()
    email = random_id()
    image_upload["email"] = email
    resp = client.post('/api/process/upload_image', json=image_upload)
    original_id = resp.json["image_id"]
    resp = client.post('/api/process/blur', json={"email": email})
    resp = client.post('/api/process/confirm', json=resp.json)
    blurred_id = resp.json["image_id"]
    resp = client.get(
        '/api/user/get_updated_uploads/{}'.format(email))
    images = resp.json
    assert len(images) == 1 and images[0]["image_id"] == blurred_id


def _check_image(img_obj):
    if len(img_obj.shape) != 3:
        return False
    if img_obj.shape[2] != 3:
        return False
    if not ((img_obj >= 0).all() and (img_obj <= 255).all()):
        return False
    return True
