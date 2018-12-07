import binascii
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
@app.route("/api/image/get_image", methods=["GET"])
def get_image():
    """
    Obtains image from database based on ID.
    Args:
        image_id: ID of the image to get.
    """
    image_id = request.args.get('id', default=None, type=str)
    if not image_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    image = db.find_image(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_parent", methods=["GET"])
def get_image_parent():
    """
    Obtains the parent of the image given an ID.
    Returns:
        object: history of the image.
    """
    image_id = request.args.get('id', default=None, type=str)
    if not image_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    image = db.find_image_parent(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_child", methods=["GET"])
def get_image_child():
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    image_id = request.args.get('id', default=None, type=str)
    if not image_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    image = db.find_image_child(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_history", methods=["GET"])
def get_image_history():
    """
    Obtains the entire history of the image in terms of IDs.
    Returns:
        object: history of the image.
    """
    image_id = request.args.get('id', default=None, type=str)
    if not image_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    image = db.find_image(image_id)
    return jsonify(image.process_history)


@app.route("/api/image/get_image_description", methods=["GET"])
def get_image_description():
    """
    Obtains the description of the image.
    Less expensive than getting whole image.
    Returns:
        str: Description of the image.
    """
    image_id = request.args.get('id', default=None, type=str)
    if not image_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    image = db.find_image(image_id)
    return jsonify(image.description)


# ---------- get user stuff ----------
@app.route("/api/user/get_user", methods=["GET"])
def get_user():
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


@app.route("/api/user/get_original_uploads", methods=["GET"])
def get_original_uploads():
    """
    Gets all root image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: root image ids.
    """
    user_id = request.args.get('id', default=None, type=str)
    if not user_id:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(user_id)
    return jsonify(list(user.uploads.keys()))


@app.route("/api/user/get_updated_uploads", methods=["GET"])
def get_updated_uploads(user_id):
    """
    Gets all updated image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: updated image ids.
    """
    user_id = request.args.get('id', default=None, type=str)
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
        image_id: ID of the current image to be processed.
        user_id: ID of the current user.
        image_data: base64 representation of image.

    Returns:
        object: New hist eq'd image.
    """
    # should take the current image with all info
    content = request.get_json()
    new_image = _process_image_post(content)
    new_image["image_data"], new_image["processing_time"] = \
        Processing(content["image_data"]).hist_eq
    new_image["process"] = "hist_eq"
    added_image = db.add_image(content["user_id"], new_image)
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
    new_image = _process_image_post(content)
    new_image["image_data"], new_image["processing_time"] = \
        Processing(content["image_bytes"]).contrast_stretch
    new_image["process"] = "contrast_stretch"
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Does rev video? lolidk
    Args:
        image_id: ID of the current image to be processed.
        user_id: ID of the current user.
        image_data: base64 representation of image.

    Returns:
        object: Reversed video.
    """
    content = request.get_json()
    new_image = _process_image_post(content)
    new_image["image_data"], new_image["processing_time"] = \
        Processing(content["image_data"]).reverse_video
    new_image["process"] = "reverse_video"
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/sharpen", methods=["POST"])
def post_image_sharpen():
    """
    Takes CURRENT image and performs image sharpen on whole image.
    Args:
        image_id: ID of the current image to be processed.
        user_id: ID of the current user.
        image_data: base64 representation of image.

    Returns:
        object: sharpened image.
    """
    content = request.get_json()
    new_image = _process_image_post(content)
    new_image["image_data"], new_image["processing_time"] = \
        Processing(content["image_data"]).sharpen
    new_image["process"] = "sharpen"
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/blur", methods=["POST"])
def post_image_blur():
    """
    Takes CURRENT image and performs image blur on whole image.
    Args:
        image_id: ID of the current image to be processed.
        user_id: ID of the current user.
        image_data: base64 representation of image.

    Returns:
        object: blurred image.
    """
    content = request.get_json()
    new_image = _process_image_post(content)
    new_image["image_data"], new_image["processing_time"] = \
        Processing(content["image_data"]).blur
    new_image["process"] = "blur"
    added_image = db.add_image(content["user_id"], content)
    return jsonify(added_image)


def _process_image_post(content):
    """
    Checks if the post content is correct and makes associated links.
    Args:
        content: User post data.

    Returns:

    """
    if not content:
        return error_handler(400, "Insufficient post.", "ValueError")
    if "image_id" not in content.keys():
        return error_handler(400, "must contain image_id", "AttributeError")
    if "image_data" not in content.keys():
        return error_handler(400, "must contain image_data", "AttributeError")

    new_image = content
    new_image["parent_id"] = content["image_id"]
    new_image["image_id"] = random_id()
    return new_image


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
