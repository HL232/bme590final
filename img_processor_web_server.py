import io
import re
import cv2
import base64
import imageio
from random import choice
from string import ascii_uppercase
from flask import Flask, request, jsonify

from processing import Processing
from database import ImageProcessingDB

app_name = "image_processor"
app = Flask(app_name)

# testing using DM
db = ImageProcessingDB()

@app.after_request 
def after_request(response): 
    response.headers.add('Access-Control-Allow-Origin', '*') 
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') 
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE') 
    return response


# ---------- get stuff ----------
# ---------- get image stuff ----------
@app.route("/api/image/get_current_image/<user_id>", methods=["GET"])
def get_current_image(user_id):
    """
    Obtains image from database based on ID.
    Args:
        user_id: ID of the image to get.
    """
    if not user_id:
        return error_handler(400, "Must include user id.", "AttributeError")
    image = db.get_current_image(user_id)
    image = db.image_to_json(image)
    return jsonify(image)


@app.route("/api/image/get_previous_image/<user_id>", methods=["GET"])
def get_previous_image(user_id):
    """
    Obtains the parent of the image given an ID.
    Returns:
        object: history of the image.
    """
    if not user_id:
        return error_handler(400, "Must include user id.", "AttributeError")
    current_image = db.get_current_image_id(user_id)
    image = db.find_image_parent(current_image, user_id)
    image = db.image_to_json(image)
    db.update_user_current(image["user_id"], image["image_id"])
    return jsonify(image)


@app.route("/api/image/get_next_image/<user_id>", methods=["GET"])
def get_next_image(user_id):
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    if not user_id:
        return error_handler(400, "Must include user id.", "AttributeError")
    curr_image_id = db.get_current_image_id(user_id)
    child_ids = db.find_image_child(curr_image_id, user_id)

    # if there are multiple, just pick the first one?
    if not child_ids:
        return None
    image = db.find_image(child_ids[0], user_id)
    image = db.image_to_json(image)
    db.update_user_current(image["user_id"], image["image_id"])

    return jsonify(image)


# ---------- get user stuff ----------
@app.route("/api/user/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Gets the user based on id
    Args:
        user_id: user to find.

    Returns:
        dict: user in database.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(user_id)
    return jsonify(user)


@app.route("/api/user/get_original_upload_ids/<user_id>", methods=["GET"])
def get_original_upload_ids(user_id):
    """
    Gets all root image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: root image ids.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(user_id)
    return jsonify(list(user.uploads.keys()))


@app.route("/api/user/get_updated_upload_ids/<user_id>", methods=["GET"])
def get_updated_upload_ids(user_id):
    """
    Gets all updated image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: updated image ids.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")

    user = db.find_user(user_id)
    updated_list = []
    for root in user.uploads.keys():
        updated_list.append(user.uploads[root])

    return jsonify(updated_list)


@app.route("/api/user/get_upload_filenames/<user_id>", methods=["GET"])
def get_upload_filenames(user_id):
    """
    Gets all root image names from a user.
    Args:
        user_id: user to find.

    Returns:
        dict: image names associated with root image.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(user_id)
    names = {}
    for image in user.uploads.keys():
        names[image.id] = image.name
    return jsonify(names)


@app.route("/api/user/get_original_uploads/<user_id>", methods=["GET"])
def get_original_uploads(user_id):
    """
    Gets all root/original images from a user.
    Args:
        user_id: user to find.

    Returns:
        list: root images.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    original_uploads = db.get_all_original_images(user_id)
    original_upload_json = []
    for upload in original_uploads:
        original_upload_json.append(db.image_to_json(upload))
    return jsonify(original_upload_json)


@app.route("/api/user/get_updated_uploads/<user_id>", methods=["GET"])
def get_updated_uploads(user_id):
    """
    Gets all updated images from a user.
    Args:
        user_id: user to find.

    Returns:
        list: updated images.
    """
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    updated_uploads = db.get_all_original_images(user_id)
    updated_json = []
    for upload in updated_uploads:
        updated_json.append(db.image_to_json(upload))
    return jsonify(updated_json)


# ----------------------------- post stuff ---------------------------

@app.route("/api/process/upload_image", methods=["POST"])
def post_upload_image():
    """
    Uploads a NEW image into the database to process.
    Args:
        user_id: ID of the current user.
        image_data: base64 representation of image.
    Returns:
        object: uploaded image object.
    """
    content = request.get_json()
    if not content:
        return error_handler(400, "Insufficient post.", "ValueError")
    if "image_data" not in content.keys():
        return error_handler(400, "must include image_data", "AttributeError")
    if "user_id" not in content.keys():
        return error_handler(400, "must include user_id", "AttributeError")
    if type(content["user_id"]) != str:
        return error_handler(400, "user_id must be type str", "TypeError")
    if "filename" not in content.keys():
        return error_handler(400, "must include filename", "AttributeError")
    if type(content["filename"]) != str:
        return error_handler(400, "filename must be type str", "TypeError")

    image = b64str_to_numpy(content["image_data"])
    content["width"] = image.shape[0]
    content["height"] = image.shape[1]
    content["image_id"] = random_id()
    content["process"] = "upload"
    content["processing_time"] = -1
    content["format"] = "None"

    image = db.add_image(content["user_id"], content)
    return jsonify(image)  # with included ID


@app.route("/api/process/confirm", methods=["POST"])
def post_confirm_image():
    """
    Adds the image to the user.
    Returns:
        dict: Image that as associated with user.
    """
    content = request.get_json()
    if not _verify_confirm_image(content):
        return error_handler(400, "Insufficient Inputs", "AttributeError")
    # must contain image_data, user_id
    added_image = db.add_image(content["user_id"], content)
    return jsonify(added_image)


def _verify_confirm_image(image):
    """
    Confirms that all necessary attributes are present at image add.
    Args:
        image (dict): Image object to be added.

    Returns:
        bool: Whether or not the image object is valid.
    """
    req = ['child_ids', 'processing_history', 'parent_id',
           'description', 'processing_time', 'format', 'process',
           'user_id', 'width', 'image_id', 'height', 'image_data']
    if set(req).issubset(set(image.keys())):
        return True
    return False


def _link_new_image(current_image):
    """
    Makes associated links.
    Args:
        current_image: current image of the user/post data.

    Returns:
        dict: Dict with linked ids.
    """
    new_image = db.image_to_json(current_image)
    new_image["user_id"] = current_image.user_id
    new_image["parent_id"] = current_image.image_id
    new_image["image_id"] = random_id()
    return new_image


def _populate_image_meta(new_image, image_data):
    """
    Populates an existing dict with image meta information.
    Args:
        new_image (dict):
        image_data (np.ndarray): image data in RGB

    Returns:
        dict: dict with image meta information

    """
    new_image["width"] = image_data.shape[0]
    new_image["height"] = image_data.shape[1]
    new_image["format"] = "None"
    return new_image


@app.route("/api/process/hist_eq/<user_id>", methods=["GET"])
def get_hist_eq(user_id):
    """
    Takes CURRENT image and performs histogram eq on image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: New hist eq'd image.
    """
    # should take the current image with all info
    ##content = request.get_json()
    # grab the user's current image.
    user_image_id = db.get_current_image_id(user_id)
    current_image = db.find_image(user_image_id, user_id)
    new_image = _link_new_image(current_image)
    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).hist_eq()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data)

    new_image["process"] = "hist_eq"
    return jsonify(new_image)


@app.route("/api/process/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    """
    Takes CURRENT image and performs contrast stretch on image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: New contrast stretched image.
    """
    content = request.get_json()
    p_low = request.args.get("l", 10)
    p_high = request.args.get("h", 90)
    percentile = (p_low, p_high)

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)
                   ).contrast_stretch(percentile)
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "contrast_stretch"
    return jsonify(new_image)


@app.route("/api/process/log_compression", methods=["POST"])
def post_image_log_compression():
    """
    Takes CURRENT image and performs log compression on image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: New log compressed image.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).log_compression()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "log_compression"
    return jsonify(new_image)


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Inverse the intensities of a grayscale image.
    Args:
        user_id: ID of the current user.

    Returns:
        dict: image with inverted intensities.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).reverse_video()
    new_image = _populate_image_meta(new_image, image_data)
    # maybe something e lse
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "reverse_video"
    return jsonify(new_image)


@app.route("/api/process/sharpen", methods=["POST"])
def post_image_sharpen():
    """
    Takes CURRENT image and performs image sharpen on whole image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: sharpened image.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).sharpen()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "sharpen"
    return jsonify(new_image)


@app.route("/api/process/blur", methods=["POST"])
def post_image_blur():
    """
    Takes CURRENT image and performs image blur on whole image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: blurred image.
    """
    content = request.get_json()
    sigma = request.args.get("s", 5)

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).blur(sigma)
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "blur"
    return jsonify(new_image)


@app.route("/api/image/search_image", methods=["POST"])
def post_search_image():
    """
    Looks for an image that the user uploaded. Filters can be included.
    Returns:
        object:
    """
    # TODO: Still not implemented in database!
    pass


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


def error_handler(status_code, msg, error_type):
    """
    Handles errors to send back to requester.
    Args:
        status_code: The status code, standard.
        msg: Message to send.
        error_type: Error type if raises exception.

    Returns:
        dict: Error message information.

    """
    error_msg = {
        "status_code": status_code,
        "msg": msg,
        "error_type": error_type
    }
    return jsonify(error_msg)


def random_id(length=10):
    """
    Generates random alpha-numeric ID.
    Returns:
        str: alpha-numeric ID
    """
    return ''.join(choice(ascii_uppercase) for _ in range(length))


def get_app():
    """
    Gets the app (for testing).
    Returns:
        object: Flask application object.
    """
    return app


if __name__ == "__main__":
    app.run(host="127.0.0.1")
