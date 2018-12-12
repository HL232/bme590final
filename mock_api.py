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


def numpy_to_b64str(img, format="JPG"):
    """
    Converts a numpy array into a base 64 string
    Args:
        img (np.array):

    Returns:
        str: base 64 representation of the numpy array/image.

    """
    if _should_reverse_image(format):
        # flip for cv conversion, only some file formats
        img = img[..., ::-1]
    _, img = cv2.imencode('.jpg', img)  # strips header
    image_base64 = base64.b64encode(img)
    base64_string = image_base64.decode('utf-8')  # convert to string
    return base64_string


def _should_reverse_image(format):
    should_reverse = ["JPG"]
    if format in should_reverse:
        return True
    else:
        return False


def b64str_to_numpy(b64_img):
    """
    Converts a b64str to numpy. Strips headers.
    Args:
        b64_img (str): base 64 representation of an image.

    Returns:
        np.ndarray: numpy array of image.

    """
    b64_image, _ = _get_b64_format(b64_img)
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    np_img = imageio.imread(image_buf, format="JPG")
    return np_img


def _get_b64_format(b64_img):
    split = b64_img.split("base64,")  # get rid of header
    image_format = None
    if len(split) == 2:
        b64_img = split[1]
        image_format = _determine_format(split[0])
    else:
        b64_img = split[0]
    return b64_img, image_format


def _determine_format(format_string: str):
    """
    Determines file format from a string. Could be header/ext.
    Args:
        format_string: Header or file extension.

    Returns:
        str: Type of the image.
    """
    formats = ["PNG",
               "TIF", "TIFF",
               "JPG", "JPEG"]
    for format in formats:
        if format in format_string.upper():
            if "JPEG" in format_string.upper():
                return "JPG"
            if "TIF" in format_string.upper():
                return "TIFF"
            return format
    return "None"


def view_image(image):
    plt.imshow(image)
    plt.show()


email = "dukebme590.imageprocessor@gmail.com"
dog_source = 'https://i.imgur.com/B15ubOP.jpg'
# dog_source = "https://i.imgur.com/2gX8HVS.png"
# dog_source = "MARBIBM.TIF"
dog_image = imageio.imread(dog_source)
# print("Original", dog_image.shape, dog_image[0][0])

image_format = _determine_format(dog_source)
image_obj = {
    "email": email,
    "image_data": numpy_to_b64str(dog_image, format=image_format),
    "filename": dog_source
}

resp = requests.post("http://127.0.0.1:5000/api/process/upload_image",
                     json=image_obj)
content = byte_2_json(resp)
# view_image(b64str_to_numpy(content[0]["image_data"]))

# blur
image_obj_2 = {"email": email}
resp = requests.post("http://127.0.0.1:5000/api/process/blur",
                     json=image_obj)
content = byte_2_json(resp)
# view_image(b64str_to_numpy(content["image_data"]))

# send_image
send_obj = {"email": email, "image_id": content["image_id"]}
requests.post("http://127.0.0.1:5000/api/process/email_image",
              json=send_obj)

"""
# attempt to confirm
resp = requests.post("http://127.0.0.1:5000/api/process/confirm", json=content)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))"""

"""
# should use the blurred image
image_obj_3 = {"email": email}
resp = requests.post("http://127.0.0.1:5000/api/process/sharpen",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# should use the non-sharpened blurred image, since not confirmed.
image_obj_5 = {"email": email}
resp = requests.post("http://127.0.0.1:5000/api/process/contrast_stretch",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
"""
