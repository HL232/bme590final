import io
import cv2
import json
import base64
import imageio
import requests
import numpy as np
from random import choice
from string import ascii_uppercase
from matplotlib import pyplot as plt
from img_processor_web_server import b64str_to_numpy


def view_image(image):
    plt.imshow(image)
    plt.show()


with open('b64testfile.txt') as f:
    data = json.load(f)

image = b64str_to_numpy(data["image_data"])
view_image(image)
print(data.keys())
