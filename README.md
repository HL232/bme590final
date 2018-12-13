# Image Processor

Authors: Matt Guptil, Howard Li, Stephen Xu

Version: 1.0.0

Licsense: MIT License (See License File)

## Introduction
This project is an image processor that is meant to be the basis of a medical imaging processor. A graphical user interface (GUI) was developed to allow a user to upload image(s) to a database. These images can be processed to produce different effects (like histogram equailzation, contrast stretching, log compression, reverse video, blurring, and sharpening) as well as the associated histogram of the images. The images are processed on a web server and the results are returned to the user's GUI, which allows the user to download the images. 

This image processor is meant to combine the functionality and scripting _prowess_ of python with the modularity and adaptability of cloud computing. The project is split into 3 primary components: image processing, web api, and a GUI, generally following the typical Model/View/Controller paradigm. For a general schematic of how our project works, check out this helpful graphic below:


![alt text](https://github.com/HL232/bme590final/blob/read-me/BME%20Software%20Final.jpg) 

## What's included in this repo:
 + `tests` folder - This contains all the unit testing python files
 + `docs, Makefile, conf.py, index.rst, make.bat` - these files are used to produce auto generated sphinx documentation
 + `.gitignore` - files that Git should not upload to github
 + `.travis.yml` - Travis CI/CD setup
 + `README.md` - this file is the readme
 + `LICENSE` - the license file which contains information on usage. Don't steal from us.
 + `config.json` - a JSON dictionary file which contains environmental variables we need
 + `database.py` - Python file that sets up our MongoDB database that stores image data
 + `img_processor_web_server` - Python file that sets up our FLASK web server that processes images and requests
 + `processing.py` - Python file that the web server uses to process images. 
 + `requirements.txt` - Python packages that need to be installed in the virtual environment to run the project

## How to run this project:
 1. Clone or download this repo locally. 
 2. Access the GUI by...
 3. From the GUI, you can upload images, download images, process images, etc
 4. To access our web server, **The server is running at BLAHHHHHHHHHHHHHHHHHHHH** The server handles POST and GET requests as defined in the `img_processor_web_server.py` file
 
# Supported Formats

## Setup
In order to set up your own instance of the webserver, it would be best to set up a virtual environment on a linux-based OS server such as Ubuntu 16.04. Using a combination of `screen`, `guicorn`, and virtual environments, deployment should take very few steps.
## Installation
First run `sudo apt-get update` and `sudo apt-get upgrade` to update all packages. Ensure that `pip` and `python3` are installed on the system, if not, run `sudo apt-get install python-pip`. To create a virtual environment, run `python3 -m venv (env)` where `(env)` is a name of your choosing. Change to the virtual environment by running `source env/bin/activate` and then run `python3 install -r requirements.txt`. After this, all necessary modules should be installed.
## Run web server
To run the `flask` web server, it's best to do so on a screen. The most painless way is to do:
```
screen -S test -d -m gunicorn --workers 4 img_processing_web_server:main
```
which creates the screen and then immediately detaches it.

# Detailed Notes on Software Logic

## GUI
Can talk about the GUI stuff here.

## MongoDB Database
Our image processor uses MongoDB to store image data. Our database contains three classes: 
 + `Image` which is a MongoModel object - This class contains the information about each individual image, including: the image ID, the file name, the array data of the image, user email, timestamps, image width/height, the image format, the description, the IDs of the parent and child images, the processing history, the processing time, and the current process.
 + `User` which is a MongoModel object - If our image processor were to have multiple users, this class contains their information. Including: user's email, upload keys, their current image they are viewing, and the process count
 + `ImageProcessingDB` which is a class that contains several functions which can modify `Image` and `User` models. `ImageProcessingDB` functions are accessed through the web server code in order to modify the `Image` and `Users` in the database.

## Web Server API Endpoints
Generally, in order to use an API endpoint, append something like `/api/endpoint_name` to the domain. In general, there are three categories for endpoints: `user`, `image`, and `process` which are fairly self-explanatory. The GUI primarily uses the `/api/process/upload`, `/api/process/next_image`, and `/api/process/previous_image` endpoints for navigation through the image history. It uses the endpoints such as `/api/process/blur` to get a blurred image, which also tells the web server that the user's current image is this blurred image.

## Image Processing
There are several different image processes performed by the web server. Each is described in the table below. Essentially, images are uploaded from the GUI to the webserver as Base64 strings. The webserver stores the image data with the database as base64. However, in order to process the image, the webserver decodes the Base64 into an Array-like object. This array object is manipulated using functions in the skimage, imageio, cv2, and matplotlib libraries to produce modified images. All of the processes described below manipulate the array data of the image to produce images that are slightly different. 

| Name          | Function      |
| ------------- | ------------- |
| Histogram Equalization         | Takes the pixel intensities and evenly distributes the intensity data throughout the entire histogram to produce a higher contrast image |
| Contrast Stretching      | Similar to histogram equalization. Takes the pixel intensities and stretches it. Different than histogram equailzation in that the intensities are not stretched for the full range of pixel intensities. |
| Log Compression | Applies a log filter to the pixel intensities. Low intensity pixels will be "log reduced" less than high intesnity pixels. |
| Reverse Video | Turns black pixels white, and white pixels black. |
| Blur |Make the image look blurry through Gaussian blurring |
| Sharpen | Sharpens the image by increasing the contrast between pixels |
