from matplotlib import pyplot as plt
from img_processor_web_server import *

domain = "vcm-7308.vm.duke.edu:5000"

# reads some images
id_list = []  # Used for downloading
image_source = ""
image = None
image_format = None
content = None

# Input your email or username
email = "blah@blah.com"


def determine_format(format_string: str):
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
    return "JPG"  # assume jpg


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


def view_image(image):
    """
    Displays an image using the matplotlib plt.show() function
    Args:
        image: the image array to show

    """
    plt.imshow(image)
    plt.axis('off')
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
