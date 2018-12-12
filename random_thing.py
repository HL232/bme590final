import io
import cv2
import json
import base64
import imageio
import requests
from matplotlib import pyplot as plt


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
    b64_img, _ = _get_b64_format(b64_img)
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    np_img = imageio.imread(image_buf, format="JPG")
    return np_img


def _get_b64_format(b64_img):
    split = b64_img.split("base64,")  # get rid of header
    if len(split) == 2:
        b64_img = split[1]
        image_format = _determine_format(split[0])
    else:
        b64_img = split[0]
        image_format = "JPG"  # assume jpg
    return b64_img, image_format


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


with open('b64testfile.txt') as f:
    data = json.load(f)
    image_b64 = data["image_data"]

image_obj = {
    "email": "szx2@duke.edu",
    "image_data": image_b64,
    "filename": "test.jpg"
}

resp = requests.post("http://127.0.0.1:5000/api/process/upload_image",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content[0]["image_data"]))
