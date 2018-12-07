import io
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


# ---------- get stuff ----------
# ---------- get image stuff ----------
@app.route("/api/image/get_image?id=<image_id>", methods=["GET"])
def get_image(image_id):
    """
    Obtains image from database based on ID.
    Args:
        image_id: ID of the image to get.
    """
    if not image_id:
        return error_handler(400, "Must include image id.", "AttributeError")
    image = db.find_image(image_id)
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
    image = db.find_image_parent(current_image["image_id"], user_id)
    return jsonify(image)


@app.route("/api/image/get_next_image?id=<user_id>", methods=["GET"])
def get_next_image(user_id):
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    if not user_id:
        return error_handler(400, "Must include user id.", "AttributeError")
    current_image = db.get_current_image_id(user_id)
    child_ids = db.find_image_child(current_image["image_id"], user_id)

    # if there are multiple, just pick the first one?
    if not child_ids:
        return None

    image = db.find_image(child_ids[0], user_id)
    return jsonify(image)


# ---------- get user stuff ----------
@app.route("/api/user/get_user?id=<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Gets the user based on id
    Args:
        user_id: user to find.

    Returns:
        dict: user in database.
    """
    user_id = request.args.get('id', default=None, type=str)
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(user_id)
    return jsonify(user)


@app.route("/api/user/get_original_uploads?id=<user_id>", methods=["GET"])
def get_original_uploads(user_id):
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


@app.route("/api/user/get_updated_uploads?id=<user_id>", methods=["GET"])
def get_updated_uploads(user_id):
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


# ----------------------------- post stuff ---------------------------
@app.route("/api/image/search_image", methods=["POST"])
def post_search_image():
    """
    Looks for an image that the user uploaded. Filters can be included.
    Returns:
        object:
    """
    # TODO: Still not implemented in database!
    pass


@app.route("/api/image/upload_image", methods=["POST"])
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

    content["processing_time"] = -1
    content["image_id"] = random_id()
    content["process"] = "upload"
    image = db.add_image(content["user_id"], content)
    return jsonify(image)  # with included ID


@app.route("/api/image/update_description", methods=["POST"])
def post_update_description():
    """
    Adds or updates the description of the image.
    Args:
        image_id: Image to update description of.
        description: Description of the image.

    Returns:
        object: updated image object.
    """
    content = request.get_json()
    if not content:
        return error_handler(400, "Insufficient post.", "ValueError")
    if "image_id" not in content.keys():
        return error_handler(400, "must have image_id.", "AttributeError")
    if "description" not in content.keys():
        return error_handler(400, "must have description.", "AttributeError")

    image = db.update_description(content["image_id"], content["description"])
    return jsonify(image)


@app.route("/api/process/hist_eq", methods=["POST"])
def post_hist_eq():
    """
    Takes CURRENT image and performs histogram eq on image.
    Args:
        user_id: ID of the current user.

    Returns:
        object: New hist eq'd image.
    """
    # should take the current image with all info
    content = request.get_json()
    # grab the user's current image.
    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).hist_eq()
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "hist_eq"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


@app.route("/api/process/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    """
    Takes CURRENT image and performs contrast stretch on image.
    Args:
        image_id: ID of the current image to be processed.
        user_id: ID of the current user.
        image_data: base64 representation of image.

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
        Processing(b64str_to_numpy(current_image.image_data)).contrast_stretch(percentile)
    # print("CSshape", image_data.shape, image_data[0][0])
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "contrast_stretch"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


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
    print("Logged shape", image_data.shape, image_data[0][0])

    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "log_compression"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Does rev video? lolidk
    Args:
        user_id: ID of the current user.

    Returns:
        object: Reversed video.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["user_id"])
    current_image = db.find_image(user_image_id, content["user_id"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).reverse_video()
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "reverse_video"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


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
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "sharpen"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


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
    new_image["image_data"] = numpy_to_b64str(image_data)
    new_image["process"] = "blur"
    added_image = db.add_image(current_image.user_id, new_image)
    return jsonify(added_image)


def _link_new_image(current_image):
    """
    Makes associated links.
    Args:
        content: User post data.

    Returns:

    """
    new_image = db.image_to_json(current_image)
    new_image["parent_id"] = current_image.image_id
    new_image["image_id"] = random_id()
    return new_image


def b64str_to_numpy(b64_img):
    byte_image = base64.b64decode(b64_img)
    image_buf = io.BytesIO(byte_image)
    np_img = imageio.imread(image_buf, format='JPG')
    i = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)
    return i


def numpy_to_b64str(img):
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
