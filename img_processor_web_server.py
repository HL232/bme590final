import io
import cv2
import json
import base64
import imageio
import sendgrid
from random import choice
from string import ascii_uppercase
from sendgrid.helpers.mail import *
from flask import Flask, request, jsonify

from processing import Processing
from database import ImageProcessingDB

app_name = "image_processor"
app = Flask(app_name)

# testing using DM
db = ImageProcessingDB()

try:
    with open("config.json", 'r') as f:
        config_info = json.load(f)
    sendgrid_API_KEY = config_info["SENDGRID_API_KEY"]
    from_email = config_info["from_email"]
except:
    pass


# ---------- get stuff ----------
# ---------- get image stuff ----------


@app.route("/api/image/get_current_image/<email>", methods=["GET"])
def get_current_image(email):
    """
    Obtains image from database based on ID.
    Args:
        email: ID of the image to get.
    """
    if not email:
        return error_handler(400, "Must include user id.", "AttributeError")
    image = db.get_current_image(email)
    image = db.image_to_json(image)
    return jsonify(image)


@app.route("/api/image/get_previous_image/<email>", methods=["GET"])
def get_previous_image(email):
    """
    Obtains the parent of the image given an ID.
    Returns:
        object: history of the image.
    """
    if not email:
        return error_handler(400, "Must include user id.", "AttributeError")
    current_image = db.get_current_image_id(email)
    image = db.find_image_parent(current_image, email)
    image = db.image_to_json(image)
    db.update_user_current(image["email"], image["image_id"])
    return jsonify(image)


@app.route("/api/image/get_next_image/<email>", methods=["GET"])
def get_next_image(email):
    """
    Obtains the child of the image given an ID.
    Returns:
        object: parent image.
    """
    if not email:
        return error_handler(400, "Must include user id.", "AttributeError")
    curr_image_id = db.get_current_image_id(email)
    child_ids = db.find_image_child(curr_image_id, email)

    # if there are multiple, just pick the first one?
    if not child_ids:
        return None
    image = db.find_image(child_ids[0], email)
    image = db.image_to_json(image)
    db.update_user_current(image["email"], image["image_id"])

    return jsonify(image)


# ---------- get user stuff ----------
@app.route("/api/user/get_user/<email>", methods=["GET"])
def get_user(email):
    """
    Gets the user based on id
    Args:
        email: user to find.
    Returns:
        dict: user in database.
    """
    if not email:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(email)
    user = db.user_to_json(user)
    return jsonify(user)


@app.route("/api/user/get_original_upload_ids/<email>", methods=["GET"])
def get_original_upload_ids(email):
    """
    Gets all root image ids from a user.
    Args:
        email: user to find.
    Returns:
        list: root image ids.
    """
    if not email:
        return error_handler(400, "Must have include id.", "AttributeError")
    user = db.find_user(email)
    return jsonify(list(user.uploads.keys()))


@app.route("/api/user/get_updated_upload_ids/<email>", methods=["GET"])
def get_updated_upload_ids(email):
    """
    Gets all updated image ids from a user.
    Args:
        email: user to find.
    Returns:
        list: updated image ids.
    """
    if not email:
        return error_handler(400, "Must have include id.", "AttributeError")

    user = db.find_user(email)
    updated_list = []
    for root in user.uploads.keys():
        updated_list.append(user.uploads[root])

    return jsonify(updated_list)


@app.route("/api/user/get_upload_filenames/<email>", methods=["GET"])
def get_upload_filenames(email):
    """
    Gets all root image names from a user.
    Args:
        email: user to find.
    Returns:
        dict: image names associated with root image.
    """
    if not email:
        return error_handler(400,
                             "Must have include email.",
                             "AttributeError")
    user = db.find_user(email)
    names = {}
    for image_id in user.uploads.keys():
        image = db.find_image(image_id, email)
        names[image_id] = image.filename
    return jsonify(names)


@app.route("/api/user/get_original_uploads/<email>", methods=["GET"])
def get_original_uploads(email):
    """
    Gets all root/original images from a user.
    Args:
        email: user to find.
    Returns:
        list: root images.
    """
    if not email:
        return error_handler(400, "Must have include id.", "AttributeError")
    original_uploads = db.get_all_original_images(email)
    original_upload_json = []
    for upload in original_uploads:
        original_upload_json.append(db.image_to_json(upload))
    return jsonify(original_upload_json)


@app.route("/api/user/get_updated_uploads/<email>", methods=["GET"])
def get_updated_uploads(email):
    """
    Gets all updated images from a user.
    Args:
        email: user to find.
    Returns:
        list: updated images.
    """
    if not email:
        return error_handler(400, "Must have include id.", "AttributeError")
    updated_uploads = db.get_all_updated_images(email)
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
        filename: the name of the file.
        email: ID of the current user.
        image_data: base64 representation of image.
    Returns:
        object: uploaded image object.
    """
    content = request.get_json()
    if not content:
        return error_handler(400, "Insufficient post.", "ValueError")
    if type(content) != list and type(content) != dict:
        return error_handler(400, "must by either dict or list of dicts")
    if "image_data" not in content.keys():
        return error_handler(400, "must include image_data", "AttributeError")
    if "email" not in content.keys():
        return error_handler(400, "must include email", "AttributeError")
    if type(content["email"]) != str:
        return error_handler(400, "email must be type str", "TypeError")
    if "filename" not in content.keys():
        return error_handler(400, "must include filename", "AttributeError")
    if type(content["filename"]) != str:
        return error_handler(400, "filename must be type str", "TypeError")

    if type(content) == dict:
        content = [content]

    uploaded_images = []
    for upload in content:
        image = b64str_to_numpy(upload["image_data"])
        upload["width"] = image.shape[0]
        upload["height"] = image.shape[1]
        upload["image_id"] = random_id()
        upload["process"] = "upload"
        upload["processing_time"] = -1
        upload["format"] = _get_b64_format(upload["image_data"])
        if "None" in upload["format"]:  # last ditch effort.
            upload["format"] = _determine_format(upload["filename"])
        image = db.add_image(upload["email"], upload)
        uploaded_images.append(db.image_to_json(image))

    return jsonify(uploaded_images)  # with included ID


@app.route("/api/process/change_image", methods=["POST"])
def post_change_image():
    """
    Changes the user's current image
    Args:
        email: user id.
        image_id: new image id to change to.
    Returns:
        dict: Image that as associated with user.
    """
    content = request.get_json()
    if "email" not in content.keys():
        error_handler(400, "needs email", "AttributeError")
    if "image_id" not in content.keys():
        error_handler(400, "needs image_id", "AttributeError")

    # must contain image_data, email
    db.update_user_current(content["email"], content["image_id"])
    image = db.find_image(content["email"], content["image_id"])
    image = db.image_to_json(image)
    return jsonify(image)


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
    # must contain image_data, email
    added_image = db.add_image(content["email"], content)
    added_image = db.image_to_json(added_image)
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
           'email', 'width', 'image_id', 'height', 'image_data']
    if set(req).issubset(set(image.keys())):
        return True
    return False


@app.route("/api/image/get_images/", methods=["POST"])
def post_get_images():
    """
    Obtains images from database based on ID.
    Args:
        image_ids: as a list of images to get.
        email: user associated with this images.
    Returns:
        list: all images.
    """
    content = request.get_json()
    email = content["email"]
    ret_images = []
    if type(content["image_ids"]) != list:
        content["iamge_ids"] = [content["iamge_ids"]]

    get_images = content["image_ids"]
    for image_id in get_images:
        image = db.find_image(image_id, email)
        ret_images.append(db.image_to_json(image))

    return jsonify(ret_images)


def _link_new_image(current_image):
    """
    Makes associated links.
    Args:
        current_image: current image of the user/post data.
    Returns:
        dict: Dict with linked ids.
    """
    new_image = db.image_to_json(current_image)
    new_image["email"] = current_image.email
    new_image["parent_id"] = current_image.image_id
    new_image["format"] = current_image.format
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
    return new_image


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


@app.route("/api/process/hist_eq", methods=["POST"])
def post_hist_eq():
    """
    Takes CURRENT image and performs histogram eq on image.
    Args:
        email: ID of the current user.
    Returns:
        object: New hist eq'd image.
    """
    # should take the current image with all info
    content = request.get_json()
    # grab the user's current image.
    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)
    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).hist_eq()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "hist_eq"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/contrast_stretch", methods=["POST"])
def post_image_contrast_stretch():
    """
    Takes CURRENT image and performs contrast stretch on image.
    Args:
        email: ID of the current user.
    Returns:
        object: New contrast stretched image.
    """
    content = request.get_json()
    p_low = request.args.get("l", 10)
    p_high = request.args.get("h", 90)
    percentile = (p_low, p_high)

    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)
                   ).contrast_stretch(percentile)
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "contrast_stretch"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/log_compression", methods=["POST"])
def post_image_log_compression():
    """
    Takes CURRENT image and performs log compression on image.
    Args:
        email: ID of the current user.
    Returns:
        object: New log compressed image.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).log_compression()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "log_compression"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/reverse_video", methods=["POST"])
def post_image_rev_video():
    """
    Inverse the intensities of a grayscale image.
    Args:
        email: ID of the current user.
    Returns:
        dict: image with inverted intensities.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).reverse_video()
    new_image = _populate_image_meta(new_image, image_data)
    # maybe something e lse
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "reverse_video"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/sharpen", methods=["POST"])
def post_image_sharpen():
    """
    Takes CURRENT image and performs image sharpen on whole image.
    Args:
        email: ID of the current user.
    Returns:
        object: sharpened image.
    """
    content = request.get_json()

    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).sharpen()
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "sharpen"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/blur", methods=["POST"])
def post_image_blur():
    """
    Takes CURRENT image and performs image blur on whole image.
    Args:
        email: ID of the current user.
    Returns:
        object: blurred image.
    """
    content = request.get_json()
    sigma = request.args.get("s", 5)

    user_image_id = db.get_current_image_id(content["email"])
    current_image = db.find_image(user_image_id, content["email"])
    new_image = _link_new_image(current_image)

    image_data, new_image["processing_time"] = \
        Processing(b64str_to_numpy(current_image.image_data)).blur(sigma)
    new_image = _populate_image_meta(new_image, image_data)
    new_image["image_data"] = numpy_to_b64str(image_data,
                                              format=new_image["format"])
    new_image["process"] = "blur"
    db.update_user_process(content["email"], new_image["process"])
    return jsonify(new_image)


@app.route("/api/process/email_image", methods=["POST"])
def post_email_image():
    """
    Takes CURRENT image and performs image blur on whole image.
    Args:
        email: email of the current user.
        image_id: id of the image to email
    Returns:
        object: response from sendgrid.
    """
    content = request.get_json()

    if "email" not in content.keys():
        return error_handler(400,
                             "must contain email", "AttributeError")
    if "image_id" not in content.keys():
        return error_handler(400,
                             "must contain image_id", "AttributeError")

    email = content["email"]
    image_id = content["image_id"]
    image = db.find_image(image_id, email)
    if image is not None:
        return email_image(image)
    return None


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
    image_format = "None"
    if len(split) == 2:
        b64_img = split[1]
        image_format = _determine_format(split[0])
    else:
        b64_img = split[0]
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


def _should_reverse_image(format):
    should_reverse = ["JPG"]
    if format in should_reverse:
        return True
    else:
        return False


def email_image(image):
    """
    Sends email regarding heart rate via Sendgrid API.
    Args:
        to_address: Address to send to
        email_subject: Subject of the email.
        email_content: Content of the email.
    Returns:
        object: API response from Sendgrid Server.
    """
    sg = sendgrid.SendGridAPIClient(apikey=sendgrid_API_KEY)
    from_email = config_info["from_email"]
    from_email = Email(from_email)
    to_email = Email(image.email)
    subject = image.filename

    attachment = Attachment()
    attachment.set_content(image.image_data)
    attachment.set_filename(image.filename)
    attachment.set_type("image/png")
    attachment.set_disposition("attachment")

    mail = Mail(from_email, subject, to_email, "")
    mail.add_attachment(attachment)

    sg.client.mail.send.post(request_body=mail.get())


def _is_valid_email(email):
    """
    Determines if the email is valid.
    Args:
        email: Email to test.
    Returns:
        bool: If the email is valid.
    """
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True


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