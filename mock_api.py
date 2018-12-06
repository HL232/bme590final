import base64
import json
import io
from matplotlib import pyplot as plt
import requests
from skimage.io import imread
import base64

ip = "http://127.0.0.1:5000"


def encode64(bytes_data):
    # encode bytes to base64 string
    base64_str = str(base64.b64encode(bytes_data), 'utf-8')
    return base64_str


"""
def decode(base64_string):
    if isinstance(base64_string, bytes):
        base64_string = base64_string.decode("utf-8")

    imgdata = base64.b64decode(base64_string)
    img = skimage.io.imread(imgdata, plugin='imageio')
    return img"""


# matt can use this directly
def read_file_as_b64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


# i need to find a way to encode from a numpy array back to b64
def numpy_to_b64(numpy_array):
    return str(base64.b64encode(numpy_array))


def view_b64_image(base64_string):
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)  # ugh
    image_bytes = base64.b64decode(base64_string)
    image_buf = io.BytesIO(image_bytes)
    i = imread(image_buf)
    plt.imshow(i)
    plt.show()

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


dog_source = 'https://s3.amazonaws.com/ifaw-pantheon/' \
             'sites/default/files/legacy/images/' \
             'resource-centre/IFAW%20Northern%20Dog.JPG'

dog_image = imread(dog_source, as_gray=True)
image_obj = {
    "user_id": "test",
    "image_data": numpy_to_b64(dog_image)
}

resp = requests.post("http://127.0.0.1:5000/api/image/upload_image", json=image_obj)
content = byte_2_json(resp)
print(content)
view_b64_image(content["image_data"])
