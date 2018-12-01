import json
import datetime
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
    pass


@app.route("/api/image/get_image_parent/<image_id>", methods=["GET"])
def get_image_parent(image_id):
    """
    Obtains the parent of the image given an ID.
    Returns:
        object: history of the image.
    """
    pass


@app.route("/api/image/get_image_child/<image_id>", methods=["GET"])
def get_image_child(image_id):
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    pass


@app.route("/api/image/get_image_history/<image_id>", methods=["GET"])
def get_image_history(image_id):
    """
    Obtains the entire history of the image in terms of IDs.
    Returns:
        object: history of the image.
    """
    pass


@app.route("/api/image/get_image_description/<image_id>", methods=["GET"])
def get_image_description(image_id):
    """
    Obtains the description of the image.
    Less expensive than getting whole image.
    Returns:
        str: Description of the image.
    """
    pass


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
    pass


@app.route("/api/user/get_original_uploads/<user_id>", methods=["GET"])
def get_original_uploads(user_id):
    """
    Gets all root image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: root image ids.
    """
    pass


@app.route("/api/user/get_updated_uploads/<user_id>", methods=["GET"])
def get_updated_uploads(user_id):
    """
    Gets all updated image ids from a user.
    Args:
        user_id: user to find.

    Returns:
        list: updated image ids.
    """
    pass


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
        object: uploaded iamge object.
    """
    pass


@app.route("/api/image/add_description", methods=["POST"])
def post_add_description():
    """
    Adds or updates the description of the image.

    Returns:
        object: updated image object.
    """
    pass


@app.route("/api/process/hist_eq", methods=["POST"])
def post_hist_eq():
    """
    Performs histogram eq on image.

    Returns:
        object: New hist eq'd image.
    """
    pass


@app.route("/api/process/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    """
    Performs contrast stretch on image.

    Returns:
        object: New contrast stretched image.
    """
    pass


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Does rev video? lolidk

    Returns:
        object: Reversed video.
    """
    pass


@app.route("/api/process/sharpen", methods=["POST"])
def post_image_sharpen():
    """
    Performs image sharpen on whole image.
    Returns:
        object: sharpened image.
    """
    pass


@app.route("/api/process/blur", methods=["POST"])
def post_image_blur():
    """
    Performs image blur on whole image.
    Returns:
        object: blurred image.
    """
    pass


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


def get_app():
    """
    Gets the app (for testing).
    Returns:
        object: Flask application object.
    """
    return app


if __name__ == "__main__":
    app.run(host="127.0.0.1")
