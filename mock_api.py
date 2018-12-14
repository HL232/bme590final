import requests
from helper import *
from img_processor_web_server import *

## Input your email or username
email = ""

# reads some images
dog_source = "images_for_testing/gray_dog.jpg"
dog_source_2 = "images_for_testing/color_dog.jpg"
dog_image = imageio.imread(dog_source)
dog_image_2 = imageio.imread(dog_source)
image_format = determine_format(dog_source)

## Uploading images
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
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj)
content = byte_2_json(resp)
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
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
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
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# it is possible to obtain all of the user's
# original and updated uploads using the
# get_updated_images or get_original_images
# endpoints
resp = requests.get(
    "http://vcm-7308.vm.duke.edu:5000"
    "/api/process/get_original_uploads")
content = byte_2_json(resp)
print("List of image IDS: ", content)

# The web server internally stores the user's current
# image and has api endpoints that allow them to scroll
# to parent and child images, thus keeping a record
# of their action history
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj)
content = byte_2_json(resp)
print("Current Image ID (first ID): ",
      content["image_id"])
# -------------
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj_2)
content = byte_2_json(resp)
print("Current Image ID (second ID): ",
      content["image_id"])
# -------------
# we can see that we do indeed go backwards,
# in this case. This creates a tree-like structure
# for the image history.
resp = requests.get(
    "http://vcm-7308.vm.duke.edu:5000/api/process/previous")
content = byte_2_json(resp)
print("New Current Image ID (first ID): ",
      content["image_id"])

content = byte_2_json(resp)

## Processing images
# upload initial image
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
# In order to process an image, the server performs
# actions on the current image, and acts upon it without
# storing it into the database/gives it to the GUI,
# They include sharpening, blurring, log compression,
# contrast stretching, histogram eq., and reverse video.
# sharpening
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/sharpen",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
# blurring
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/blur",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
# log compression
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/log_compression",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
# contrast stretching
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/contrast_stretch",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
# histogram equalization
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/hist_eq",
    json=image_obj_2)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# reverse video
# NOTE it only works for grayscale images
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/reverse_video",
    json=image_obj_2)
content = byte_2_json(resp)
print(content)
# Here is a grayscale image to test.
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/upload_image",
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))
resp = requests.post(
    "http://vcm-7308.vm.duke.edu:5000/api/process/reverse_video",
    json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

"""
filenames = []
image_data = []
for i in range(3):
    filenames.append(image_obj["filename"])
    image_data.append(image_obj["image_data"])
image_obj["email"] = image_obj["email"]
image_obj["image_data"] = image_data
image_obj["filename"] = filenames"""

"""
filename = "test_folder.zip"
image_obj = {
    "email": email,
    "image_data": zip_to_b64(filename),
    "filename": filename
}"""

ids = []
"""
for image in content:
    ids.append(image["image_id"])
    # view_image(b64str_to_numpy(image["image_data"]))
"""
# blur
image_obj_2 = {"email": email}
resp = requests.post("http://vcm-7308.vm.duke.edu:5000/api/process/reverse_video",
                     json=image_obj)
content = byte_2_json(resp)
ids.append(content["image_id"])
# view_image(b64str_to_numpy(content["histogram"]))
# attempt to confirm
resp = requests.post("http://vcm-7308.vm.duke.edu:5000/api/process/confirm", json=content)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# attempt to get zipped images
"""
zip_post = {
    "image_ids": ids,
    "email": email,
    "format": "JPG"
}
resp = requests.post("http://vcm-7308.vm.duke.edu:5000/api/image/get_images_zipped",
                     json=zip_post)
content = byte_2_json(resp)
b64_zip = content["zip_data"][0:50]
print(b64_zip)"""

"""
# should use the blurred image
image_obj_3 = {"email": email}
resp = requests.post("http://vcm-7308.vm.duke.edu:5000/api/process/sharpen",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))

# should use the non-sharpened blurred image, since not confirmed.
image_obj_5 = {"email": email}
resp = requests.post("http://vcm-7308.vm.duke.edu:5000/api/process/contrast_stretch",
                     json=image_obj)
content = byte_2_json(resp)
view_image(b64str_to_numpy(content["image_data"]))"""
