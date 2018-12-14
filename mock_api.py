import imageio
import requests
from helper import *
from img_processor_web_server import *
from matplotlib import pyplot as plt

domain = "vcm-7308.vm.duke.edu:5000"

# Input your email or username
email = "blah@blah.com"

# reads some images
id_list = []  # Used for downloading
dog_source = "images_for_testing/gray_dog.jpg"
dog_source_2 = "images_for_testing/color_dog.jpg"
dog_image = imageio.imread(dog_source)
dog_image_2 = imageio.imread(dog_source)
image_format = determine_format(dog_source)

# Uploading images
# This is an example of uploading a single image
# to the webserver. It returns a json of the
# database image and sets it as current
image_obj = {
    "email": email,
    "image_data": numpy_to_b64str(
        dog_image, format=image_format),
    "filename": dog_source
}
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj)
content = byte_2_json(resp)
id_list.append(content["image_id"])  # used for dwnlding
view_image(b64str_to_numpy(content["image_data"]))
view_image(b64str_to_numpy(content["histogram"]))

# This is an example of uploading a multiple images
# to the webserver. It returns a json of the last
# database image that was processed and sets it
# as current
image_obj_2 = {
    "email": email,
    "image_data": numpy_to_b64str(
        dog_image, format=image_format),
    "filename": dog_source
}
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# If a zip file is uploaded, it will process it
# and then return a json of the last
# database image that was processed and sets it
# as current
zip_file = "tests/images_for_testing/test_folder.zip"
image_obj = {
    "email": email,
    "image_data": zip_to_b64(zip_file),
    "filename": zip_file
}
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# it is possible to obtain all of the user's
# original and updated uploads using the
# get_updated_images or get_original_images
# endpoints
resp = requests.get(
    "http://{}/api/user/get_original_uploads/{}".format(domain, email))
# But this is too big to display in a juypter notebook

# The web server internally stores the user's current
# image and has api endpoints that allow them to scroll
# to parent and child images, thus keeping a record
# of their action history
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj)
content = byte_2_json(resp)
print("Current Image ID (first ID): ",
      content["image_id"])
# -------------
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print("Current Image ID (second ID): ",
      content["image_id"])

# we can see that we do indeed go backwards,
# in this case. This creates a tree-like structure
# for the image history.
resp = requests.get(
    "http://{}/api/image/get_previous_image/".format(domain, email))
content = byte_2_json(resp)
print("New Current Image ID (first ID): ",
      content["image_id"])

content = byte_2_json(resp)

# Processing images
# upload initial image
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))


# In order to process an image, the server performs
# actions on the current image, and acts upon it without
# storing it into the database/gives it to the GUI,
# They include sharpening, blurring, log compression,
# contrast stretching, histogram eq., and reverse video.
# sharpening
resp = requests.post(
    "http://{}/api/process/sharpen".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Original Image:')
view_image(b64str_to_numpy(content["image_data"]))
# blurring
resp = requests.post(
    "http://{}/api/process/blur".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Blur')
view_image(b64str_to_numpy(content["image_data"]))
# log compression
resp = requests.post(
    "http://{}/api/process/log_compression".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Log Compression')
view_image(b64str_to_numpy(content["image_data"]))
# contrast stretching
resp = requests.post(
    "http://{}/api/process/contrast_stretch".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Contrast Stretch')
view_image(b64str_to_numpy(content["image_data"]))
# histogram equalization
resp = requests.post(
    "http://{}/api/process/hist_eq".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Histogram Equalization')
view_image(b64str_to_numpy(content["image_data"]))

# reverse video
# NOTE it only works for grayscale images
# Here is a grayscale image to test.
resp = requests.post(
    "http://{}/api/process/upload_image".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Original Gray Image:')
view_image(b64str_to_numpy(content["image_data"]))
resp = requests.post(
    "http://{}/api/process/reverse_video".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
print('Reverse Video')
view_image(b64str_to_numpy(content["image_data"]))


# Confirming
# Notice that none of the actions done to the initial
# Image was permanent. In order to commit a to a change
# or a processing functionality, you need to confirm
confirmed = requests.post(
    "http://{}/api/process/confirm".format(domain),
    json={"email": email})
confirmed = byte_2_json(resp)
print(confirmed)

# Process count
# Every time the user does a process, it is logged.
# The count will increase, just as a record.
resp = requests.get(
    "http://{}/api/user/get_user/{}".format(domain, email))
content = byte_2_json(resp)
print(content["process_count"])

# Metadata
# Additionally, note that every single image has a
# significant amount of metadata associated with it.
# These include: parent-child relationships with other
# images, the upload timestamp, process time,
# image size, and the histogram
confirmed_2 = confirmed
del confirmed_2["image_data"]
del confirmed_2["histogram"]
print(confirmed_2)

# DOESNT WORK*******************************************************
# Downloading
# Downloading comes in several different forms: single
# or zipped in a file with a file type or your choice
# attempt to get zipped images
# --------------
# single image
# It can be converted back to a numpy array and
# subsequently saved in any type via imageio in
# a directory of the user's choosing.
image_name = "test.jpg"
payload = {
    "image_id": confirmed["image_id"],
    "email": confirmed["email"]
}
resp = requests.post(
    "http://{}/api/image/get_images".format(domain),
    json=image_obj_2)
content = byte_2_json(resp)
np_image = b64str_to_numpy(content[0]["image_data"])
imageio.imwrite(image_name)

# DOESN'T WORK******************************************************
# zip file and specific formats
zip_post = {
    "image_ids": id_list,
    "email": email,
    "format": "PNG"
}
resp = requests.post(
    "http://{}/api/image/get_images_zipped".format(domain),
    json=zip_post)
content = byte_2_json(resp)
# Now it is up to us to convert the base64 zip into a file
folder_name = "folder_here"
b64_str = content["image_data"]
b64_str = b64_str.encode('utf-8')
decoded = base64.decodebytes(b64_str)
with zipfile.ZipFile(io.BytesIO(decoded)) as f:
    f.extractall(folder_name)
    for filename in f.namelist():
        filepath = "{}/{}".format(folder_name, filename)
        ret = {}
        ext = os.path.splitext(filename)[1]
        ret["filename"] = filename
        image = imageio.imread(filepath)
