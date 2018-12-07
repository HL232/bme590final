import base64
import imageio
import json
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import requests
from io import BytesIO
import numpy as np
from skimage.io import imread
import base64
import cv2

ip = "http://127.0.0.1:5000"


def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def byte_2_json(resp):
    """
    Converts bytes to json. Raises exception if necessary.
    Args:
        resp (bytes): Response from request.

    Returns:
        dict: Json object of interest.

    """
    json_resp = json.loads(resp.content.decode('utf-8'))
    json_resp = error_catcher(json_resp)
    return json_resp


def error_catcher(json_resp: dict):
    """
    Raises appropriate exceptions from the web server.
    Args:
        json_resp: Information from the server.

    Returns:
        dict: The original dictionary if not error.

    """
    if type(json_resp) == dict and "error_type" in json_resp.keys():
        if "TypeError" in json_resp["error_type"]:
            raise TypeError(json_resp["msg"])
        if "AttributeError" in json_resp["error_type"]:
            raise AttributeError(json_resp["msg"])
        if "ValueError" in json_resp["error_type"]:
            raise ValueError(json_resp["msg"])
    return json_resp


def b64str_to_numpy(b64_img):
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    i = mpimg.imread(image_buf, format='JPG')
    return i


def numpy_to_b64str(img):
    image_base64 = base64.b64encode(img)
    base64_string = image_base64.decode('utf-8')  # convert to string
    return base64_string


def view_image(image):
    plt.imshow(image)
    plt.show()


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
             'sites/default/files/legacy/images/' \
             'resource-centre/IFAW%20Northern%20Dog.JPG'

dog_image = imageio.imread(dog_source)
_, dog_image = cv2.imencode('.jpg', dog_image)
image_obj = {
    "user_id": "test",
    "image_data": numpy_to_b64str(dog_image)
}

# resp = requests.post("http://127.0.0.1:5000/api/image/upload_image", json=image_obj)
# content = byte_2_json(resp)
test = b64str_to_numpy(image_obj["image_data"])
view_image(test)
