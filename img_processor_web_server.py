import json
import datetime
from random import choice
from string import ascii_uppercase
from flask import Flask, request, jsonify

from processing import Processing
from database import ImageProcessingDB

app_name = "image_processor"
app = Flask(app_name)
# testing in memory
# images = {}
# users = {}

# testing using DM
db = ImageProcessingDB()


# ---------- get stuff ----------
# ---------- get image stuff ----------
@app.route("/api/image/get_image/<image_id>", methods=["GET"])
def get_image(image_id):
    """
    Obtains image from database based on ID.
    Args:
        image_id: ID of the image to get.
    """
    image = db.find_image(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_parent/<image_id>", methods=["GET"])
def get_image_parent(image_id):
    """
    Obtains the parent of the image given an ID.
    Returns:
        object: history of the image.
    """
    image = db.find_image_parent(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_child/<image_id>", methods=["GET"])
def get_image_child(image_id):
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    image = db.find_image_child(image_id)
    return jsonify(image)


@app.route("/api/image/get_image_history/<image_id>", methods=["GET"])
def get_image_history(image_id):
    """
    Obtains the entire history of the image in terms of IDs.
    Returns:
        object: history of the image.
    """
    image = db.find_image(image_id)
    return jsonify(image.process_history)


@app.route("/api/image/get_image_description/<image_id>", methods=["GET"])
def get_image_description(image_id):
    """
    Obtains the description of the image.
    Less expensive than getting whole image.
    Returns:
        str: Description of the image.
    """
    image = db.find_image(image_id)
    return jsonify(image.description)


# ---------- get user stuff ----------
@app.route("/api/user/get_original_uploads/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Gets the user based on id
    Args:
        user_id: user to find.

    Returns:
        dict: user in database.
    """
    user = db.find_user(user_id)
    return jsonify(user)


@app.route("/api/user/get_original_uploads/<user_id>", methods=["GET"])
def get_original_uploads(user_id):
    """
    Gets all root image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: root image ids.
    """
    user = db.find_user(user_id)
    return jsonify(list(user.uploads.keys()))


@app.route("/api/user/get_updated_uploads/<user_id>", methods=["GET"])
def get_updated_uploads(user_id):
    """
    Gets all updated image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: updated image ids.
    """
    user = db.find_user(user_id)
    updated_list = []
    for root in user.uploads.keys():
        updated_list.append(user.uploads[root])

    return jsonify(updated_list)


# ---------- post stuff ----------
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
    Uploads an image into the database.
    Returns:
        object: uploaded image object.
    """
    content = request.get_json()
    # you need to give the id you want to set?
    # maybe it's best if the id is just randomly generated
    # as long as the client provides a parent_id if any...
    content["image_id"] = random_id()
    image = db.add_image(content["user_id"], content)
    return jsonify(image)


@app.route("/api/image/update_description", methods=["POST"])
def post_update_description():
    """
    Adds or updates the description of the image.

    Returns:
        object: updated image object.
    """
    content = request.get_json()
    if "image_id" not in content.keys():
        raise AttributeError("must have image_id.")
    if "description" not in content.keys():
        raise AttributeError("must have description.")

    image = db.update_description(content["image_id"],
                                  content["description"])
    return jsonify(image)


@app.route("/api/process/hist_eq", methods=["POST"])
def post_hist_eq():
    """
    Performs histogram eq on image.

    Returns:
        object: New hist eq'd image.
    """
    # should take the current image with all info
    content = request.get_json()
    new_image = _get_new_image_obj(content, Processing.hist_eq)
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    """
    Performs contrast stretch on image.

    Returns:
        object: New contrast stretched image.
    """
    content = request.get_json()
    new_image = _get_new_image_obj(content, Processing.contrast_stretch)
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Does rev video? lolidk

    Returns:
        object: Reversed video.
    """
    content = request.get_json()
    new_image = _get_new_image_obj(content, Processing.reverse_video)
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/sharpen", methods=["POST"])
def post_image_sharpen():
    """
    Performs image sharpen on whole image.
    Returns:
        object: sharpened image.
    """
    content = request.get_json()
    new_image = _get_new_image_obj(content, Processing.sharpen)
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


@app.route("/api/process/blur", methods=["POST"])
def post_image_blur():
    """
    Performs image blur on whole image.
    Returns:
        object: blurred image.
    """
    content = request.get_json()
    new_image = _get_new_image_obj(content, Processing.blur)
    added_image = db.add_image(content["user_id"], new_image)
    return jsonify(added_image)


def _get_new_image_obj(old_image, process):
    # change it + prepare the object for adding
    """
    Applies a process to the old image and returns addable object.
    Args:
        old_image: Old image to transform.
        process: Processing process.

    Returns:
        dict: new image obj.

    """
    new_image = old_image
    # TODO: Test these attributes
    new_image["parent_id"] = old_image["image_id"]
    new_image["image_id"] = random_id()
    new_image["image"] = process(old_image["image"])
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
