import io
import cv2
import base64
import pytest
import imageio
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


@pytest.fixture()
def flask_app():
    app = get_app()
    return app


@pytest.fixture()
def image_post():
    dog_source = 'https://i.imgur.com/B15ubOP.jpg'
    dog_image = imageio.imread(dog_source)
    image_data = numpy_to_b64str(dog_image)
    image = {
        "user_id": "",
        "image_id": "0",
        "image_data": image_data,
        "height": 100,
        "width": 100,
        "format": "png",
        "processing_time": 30,
        "process": "hist_eq",
    }
    return image


@pytest.fixture()
def image_upload():
    dog_source = 'https://i.imgur.com/B15ubOP.jpg'
    dog_image = imageio.imread(dog_source)
    image_data = numpy_to_b64str(dog_image)
    image = {
        "user_id": "",
        "image_data": image_data,
    }
    return image


def b64str_to_numpy(b64_img):
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    np_img = imageio.imread(image_buf, format='JPG')
    i = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return i


def numpy_to_b64str(img, format=".jpg"):
    _, img = cv2.imencode(format, img)  # strips header
    image_base64 = base64.b64encode(img)
    base64_string = image_base64.decode('utf-8')  # convert to string
    return base64_string


# --------------------------- tests begin --------------------------

# ----------------- Post tests ------------------------------

def test_post_upload_image(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    resp = client.post('/api/process/upload_image', json=image_upload)
    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(resp.json["user_id"])
    assert _check_image(db_image) and \
        user.current_image == resp.json["image_id"]


def test_post_hist_eq(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/hist_eq',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_image_contrast_stretch(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/contrast_stretch',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_image_log_compression(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/sharpen',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_image_reverse_video(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/reverse_video',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_image_sharpen(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/sharpen',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_image_blur(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image', json=image_upload)
    resp = client.post('/api/process/blur',
                       json={"user_id": image_upload["user_id"]})

    db_image = b64str_to_numpy(resp.json["image_data"])
    assert _check_image(db_image)


def test_post_confirm(flask_app, image_upload):
    client = flask_app.test_client()
    image_upload["user_id"] = random_id()
    client.post('/api/process/upload_image',
                json=image_upload)
    resp = client.post('/api/process/blur',
                       json={"user_id": image_upload["user_id"]})
    resp = client.post('/api/process/confirm',
                       json=resp.json)

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(resp.json["user_id"])
    assert _check_image(db_image) and \
        user.current_image == resp.json["image_id"]


# ---------------- get tests ------------------------------

def test_get_current_image(flask_app, image_upload):
    client = flask_app.test_client()
    user_id = random_id()
    image_upload["user_id"] = user_id
    resp = client.post('/api/process/upload_image', json=image_upload)
    resp = client.get('/api/image/get_current_image/{}'.format(user_id))

    db_image = b64str_to_numpy(resp.json["image_data"])
    user = db.find_user(image_upload["user_id"])
    current_id = user.current_image

    assert _check_image(db_image) and \
        current_id == resp.json["image_id"]


def test_get_previous_image(flask_app, image_upload):
    client = flask_app.test_client()
    user_id = random_id()
    image_upload["user_id"] = user_id
    original = client.post('/api/process/upload_image', json=image_upload)
    original = original.json

    resp = client.post('/api/process/blur', json={"user_id": user_id})
    client.post('/api/process/confirm', json=resp.json)

    # should set back to uploaded image
    resp = client.get('/api/image/get_previous_image/{}'.format(user_id))
    prev_image = resp.json

    user = db.find_user(user_id)
    curr_image = user.current_image

    assert prev_image["image_id"] == original["image_id"] \
        and curr_image == prev_image["image_id"]


def test_get_next_image(flask_app, image_upload):
    client = flask_app.test_client()
    user_id = random_id()
    image_upload["user_id"] = user_id
    resp = client.post('/api/process/upload_image', json=image_upload)
    original = resp.json

    resp = client.post('/api/process/blur', json={"user_id": user_id})
    resp = client.post('/api/process/confirm', json=resp.json)
    blurred_image = resp.json
    resp = client.get('/api/image/get_previous_image/{}'.format(
        image_upload["user_id"]))
    previous_image = resp.json

    resp = client.get('/api/image/get_next_image/{}'.format(
            previous_image["user_id"]))
    next_image = resp.json

    user = db.find_user(image_upload["user_id"])
    current_id = user.current_image

    assert original["image_id"] == previous_image["image_id"] \
        and next_image["image_id"] == blurred_image["image_id"] \
        and current_id == blurred_image["image_id"]


def test_get_user(flask_app, image_post):
    client = flask_app.test_client()
    image_id = random_id()
    resp = client.get(
        '/api/user/get_user/{}'.format(image_id))


def test_get_original_uploads(flask_app, image_post):
    client = flask_app.test_client()
    image_id = random_id()
    resp = client.get(
        '/api/user/get_original_uploads/{}'.format(image_id))


def test_get_updated_uploads(flask_app, image_post):
    client = flask_app.test_client()
    image_id = random_id()
    resp = client.get(
        '/api/user/get_updated_uploads/{}'.format(image_id))


def _check_image(img_obj):
    if type(img_obj) != np.ndarray:
        return False
    if len(img_obj.shape) != 3:
        return False
    if img_obj.shape[2] != 3:
        return False
    if not ((img_obj >= 0).all() and (img_obj <= 255).all()):
        return False
    return True
