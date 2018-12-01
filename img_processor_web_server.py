import json
import datetime

from database import ImageProcessingDB
from flask import Flask, request, jsonify

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


@app.route("/api/image/get_image_history/<image_id>", methods=["GET"])
def get_image_history(image_id):
    pass


@app.route("/api/image/get_image_info/<image_id>", methods=["GET"])
def get_image_info(image_id):
    pass


# ---------- get user stuff ----------
@app.route("/api/user/get_original_uploads/<user_id>", methods=["GET"])
def get_original_uploads(user_id):
    pass


@app.route("/api/user/get_updated_uploads/<user_id>", methods=["GET"])
def get_updated_uploads(user_id):
    pass


@app.route("/api/user/get_email/<user_id>", methods=["GET"])
def get_user_email(user_id):
    pass


# ---------- post stuff ----------
@app.route("/api/image/add_image", methods=["POST"])
def post_add_image():
    pass


@app.route("/api/image/add_tags", methods=["POST"])
def post_add_tags():
    pass


@app.route("/api/image/hist_eq", methods=["POST"])
def post_hist_eq():
    pass


@app.route("/api/image/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    pass


@app.route("/api/image/reverse_video", methods=["POST"])
def post_image_rev_video():
    pass


@app.route("/api/image/sharpen", methods=["POST"])
def post_image_sharpen():
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
