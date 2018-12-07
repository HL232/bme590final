import json
import pytest
import datetime
from random import choice
from string import ascii_uppercase
from processing import Processing

from img_processor_web_server import get_app


def random_id():
    return ''.join(choice(ascii_uppercase) for _ in range(10))


@pytest.fixture()
def flask_app():
    app = get_app()
    return app


@pytest.fixture()
def image_info():
    image = {
        "image_id": "0",
        "image": "test",
        "height": 100,
        "width": 100,
        "format": "png",
        "processing_time": 30,
        "process": "hist_eq",
    }
    return image


def test_get_image(flask_app, image_info):
    client = flask_app.test_client()
    image_id = random_id()
    resp = client.get('/api/image/get_image/{}'.format(image_id))
    # assert resp.status_code == 200


def test_post_upload_image(flask_app, image_info):
    client = flask_app.test_client()
    resp = client.post('/api/image/upload_image', json=image_info)
    # assert resp.json["status_code"] == 200
