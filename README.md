# Image Processor

Authors: Matt Guptil, Howard Li, Stephen Xu

Version: 1.0.0

Licsense: MIT License (See License File)

## Introduction
This image processor is meant to combine the functionality and scripting _prowess_ of python with the modularity and adaptability of cloud computing. The project is split into 3 primary components: image processing, web api, and a GUI, generally following the typical Model/View/Controller paradigm. For a general schematic of how our project works, check out this helpful graphic below:


        bme590final/BME Software Final.jpg
      
      
## Usage
The GUI can be accessed via...
## Supported Formats


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

# Web Server API Endpoints
Generally, in order to use an API endpoint, append something like `/api/endpoint_name` to the domain. In general, there are three categories for endpoints: `user`, `image`, and `process` which are fairly self-explanatory. The GUI primarily uses the `/api/process/upload`, `/api/process/next_image`, and `/api/process/previous_image` endpoints for navigation through the image history. It uses the endpoints such as `/api/process/blur` to get a blurred image, which also tells the web server that the user's current image is this blurred image.

# Image Processing
There are several different image processes performed by the web server. Each will be described in the table below. The library used is __ which generally takes things in ---- talk about how it's processed.

| Name          | Function      |
| ------------- | ------------- |
| Histogram Equalization         | right-aligned |
| Contrast Stretching      | centered      |
| Log Compression | are neat      |
| Reverse Video | are neat      |
| Sharpen | are neat      |
| Blur | are neat      |

# GUI
Can talk about the GUI stuff here.

At a minimum, you image processor should do the following:
* Provide a [graphical] user interface that will allow a user to select an image, list of
  images, or a zip archive of images that will be uploaded to your web-server,
  perform necessary preprocessing steps, and then issue a RESTful API request
  to your cloud service for further processing.
* Your [graphical] user interface will have a choice of processing steps to perform on each
  uploaded image, including:
  + Histogram Equalization [default]
  + Contrast Stretching
  + Log Compression
  + Reverse Video
  + Others of your choice!
* A cloud-based web service that exposes a well-crafted RESTful API that will
  implement the image processing methods specified above (checkout out
  [scikit-image](http://scikit-image.org/) to make your life easier on the image processing algorithms!).
* A database should be implemented in some form to do one or more of the following:
  + Store previous user actions / metrics (e.g. how many times has a user run Histogram Equalization, 
  latency for running different processing tasks, etc). 
  + Store uploaded images and timestamps for a user
  + Store processed images (along with what processing was applied) and timestamps for a user
  + Another use case you choose.
* Your user interface should also provide:
  + An option to display and compare the original and processed images.
  + An option to download the image(s) in one of the following formats:
    - JPEG
    - PNG
    - TIFF
  If multiple images are to be downloaded, they should be downloaded as a zip archive.
  + Display histograms of the image color / intensity values of the original and processed images.
  + Display useful metadata, including:
    - Timestamp when uploaded
    - Time to process the image(s)
    - Image size (e.g., X x Y pixels)
