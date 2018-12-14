import os
import io
import cv2
import json
import base64
import random
import zipfile
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


def random_id(length=10):
    """
    Generates random alpha-numeric ID.
    Returns:
        str: alpha-numeric ID
    """
    return ''.join(choice(ascii_uppercase) for _ in range(length))


def b64str_zip_to_images(b64_str, folder_name):
    b64_str = b64_str.encode('utf-8')
    decoded = base64.decodebytes(b64_str)

    # makes a folder
    ret_images = []
    os.makedirs(folder_name, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(decoded)) as f:
        f.extractall("temp")

        for filename in f.namelist():
            filepath = "temp/{}".format(filename)
            ret = {}
            ext = os.path.splitext(filename)[1]
            ret["filename"] = filename
            image = imageio.imread(filepath)
            ret["image_data"] = numpy_to_b64str(image)
            ret["width"] = image.shape[0]
            ret["height"] = image.shape[1]
            ret["image_id"] = random_id()
            ret["process"] = "upload"
            ret["processing_time"] = -1
            ret["format"] = _determine_format(ext)
            ret_images.append(ret)

    # os.removedirs(folder_name)
    return ret_images


email = "dukebme590.imageprocessor@gmail.com"
dog_source = 'https://i.imgur.com/B15ubOP.jpg'
# dog_source = "https://i.imgur.com/2gX8HVS.png"
# dog_source = "MARBIBM.TIF"
dog_source = "images_for_testing/gray_dog.jpg"
dog_image = imageio.imread(dog_source)
# print("Original", dog_image.shape, dog_image[0][0])


image_format = _determine_format(dog_source)
image_obj = {
    "email": email,
    "image_data": numpy_to_b64str(dog_image, format=image_format),
    "filename": dog_source
}

"""
filenames = []
image_data = []
for i in range(3):
    filenames.append(image_obj["filename"])
    image_data.append(image_obj["image_data"])
image_obj["email"] = image_obj["email"]
image_obj["image_data"] = image_data
image_obj["filename"] = filenames"""


"""
filename = "test_folder.zip"
image_obj = {
    "email": email,
    "image_data": zip_to_b64(filename),
    "filename": filename
}"""

resp = requests.post(
    "http://127.0.0.1:5000/api/process/upload_image",
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["histogram"]))

ids = []
"""
for image in content:
    ids.append(image["image_id"])
    # view_image(b64str_to_numpy(image["image_data"]))
"""
# blur
image_obj_2 = {"email": email}
resp = requests.post("http://127.0.0.1:5000/api/process/reverse_video",
                     json=image_obj)
content = byte_2_json(resp)
ids.append(content["image_id"])
# view_image(b64str_to_numpy(content["histogram"]))
# attempt to confirm
resp = requests.post("http://127.0.0.1:5000/api/process/confirm", json=content)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# attempt to get zipped images
"""
zip_post = {
    "image_ids": ids,
    "email": email,
    "format": "JPG"
}
resp = requests.post("http://127.0.0.1:5000/api/image/get_images_zipped",
                     json=zip_post)
content = byte_2_json(resp)
b64_zip = content["zip_data"][0:50]
print(b64_zip)"""

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
view_image(b64str_to_numpy(content["image_data"]))"""
