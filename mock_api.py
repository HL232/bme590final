import io
import cv2
import json
import base64
import imageio
import requests
from random import choice
from string import ascii_uppercase
from matplotlib import pyplot as plt

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
    np_img = imageio.imread(image_buf, format='JPG')
    i = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return i


def numpy_to_b64str(img, format=".jpg"):
    _, img = cv2.imencode(format, img)  # strips header
    image_base64 = base64.b64encode(img)
    base64_string = image_base64.decode('utf-8')  # convert to string
    return base64_string


def view_image(image):
    plt.imshow(image)
    plt.show()


user_id = "test"
dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
             'sites/default/files/legacy/images/' \
             'resource-centre/IFAW%20Northern%20Dog.JPG'

dog_image = imageio.imread(dog_source)
# print("Original", dog_image.shape, dog_image[0][0])

image_obj = {
    "user_id": user_id,
    "image_data": numpy_to_b64str(dog_image)
}

resp = requests.post("http://127.0.0.1:5000/api/image/upload_image",
                     json=image_obj)
content = byte_2_json(resp)

# blur
image_obj_2 = {"user_id": user_id}
resp = requests.post("http://127.0.0.1:5000/api/process/blur",
                     json=image_obj)
content = byte_2_json(resp)
# attempt to confirm
resp = requests.post("http://127.0.0.1:5000/api/process/confirm", json=content)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# should use the blurred image
image_obj_3 = {"user_id": user_id}
resp = requests.post("http://127.0.0.1:5000/api/process/sharpen",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# should use the non-sharpened blurred image, since not confirmed.
image_obj_5 = {"user_id": user_id}
resp = requests.post("http://127.0.0.1:5000/api/process/contrast_stretch",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
