# Image Processor

Authors: Matt Guptil, Howard Li, Stephen Xu

Version: 1.0.0

Licsense: MIT License (See License File)

**Narrated Demo 1 of prototype 1 can be viewed at: https://drive.google.com/file/d/1PUV9RYPAMvBxtW2BhL8S4apdYqe0DzgF/view?usp=sharing** 

**Unnarrated Demo 2 of final version can be viewed at: https://drive.google.com/open?id=1M-ARBRLB8Stkfzxn0Wz2ARGeCt6xRW6C**

Because we used ReactUI, we are not 100% sure of it's reliability. Therefore, we have also created a Jupyter Notebook Walkthrough to explain how our image processor works, with some examples. (https://github.com/HL232/bme590final/blob/master/Image_Processor_Jupyter_Notebook.ipynb) We kindly ask that you look kindly on our front-end UI as an opportunity for extra credit since we believe we went above and beyond in attempting to use it. 

## Introduction
This project is an image processor that is meant to be the basis of a medical imaging processor. A graphical user interface (GUI) was developed to allow a user to upload image(s) to a database. These images can be processed to produce different effects (like histogram equailzation, contrast stretching, log compression, reverse video, blurring, and sharpening) as well as the associated histogram of the images. The images are processed on a web server and the results are returned to the user's GUI, which allows the user to download the images. The project is split into 3 primary components: image processing, web api, and a GUI, generally following the typical Model/View/Controller paradigm. For a general schematic of how our project works, check out this helpful graphic below:


![alt text](https://github.com/HL232/bme590final/blob/read-me/BME%20Software%20Final.jpg) 

## How to run this project:
Note that this is a development version of our application, not a production version, so you will have to run this project manually. In the future, we would like to learn how to deploy an app with a front-end ReactUI and a Python/Flask backend. 

 1. Clone or download this repo locally. 
 2. **Note that our GUI is set to send API requests to a server running at http://vcm-7308.vm.duke.edu:5000/ blahblahblah, but you still need to run the ReactJS GUI locally**
 3. To run ReactJS GUI Locally:
  *	Make sure Chrome is set as your default browser
  *	Open Terminal/Command Prompt
  *	Navigate to bme590final/react-ui
  *	Once inside this folder type `npm install` and press enter
  *	Wait for Install to complete
  *	Once completed type `npm run start`
  *	This will open the GUI in a Chrome Web Browser

 4. From the GUI, you can upload images, download images, process images, etc. **The GUI runs rather slowly. Use smaller images for maximum speed**
 
 **IMPORTANT: We are using mLab for our MongoDB database. The free tier only gives us 500 MB of storage. When we get to 300 MB our application slows down significantly. If you go over 500 MB of data, our application crashes. IF THE SERVER GOES DOWN, OR IF mLab FILLS UP, CONTACT STEPHEN (stephen.xu@duke.edu)**

## What's included in this repo:
 + `docs` folder - this folder has the rst files needed to produce Sphinx documentation
 + `images_for_test` folder - this folder contains sample images from our image processor. These images are used for unit testing
 + `react-ui` folder - This contains all the JavsScript files for our front end UI
 + `tests` folder - This contains all the unit testing python files
 + `.gitignore` - files that Git should not upload to github
 + `.travis.yml` - Travis CI/CD setup
 + `helper.py, Image_Processor_Jupyter_Notebook.ipyynb` - These files are used in a "walkthrough" explaining how our webserver works. 
 + `LICENSE` - the license file which contains information on usage. Don't steal from us.
 + `README.md` - this file is the readme
 + `config.json` - a JSON dictionary file which contains environmental variables we need
 + `database.py` - Python file that sets up our MongoDB database that stores image data
 + `img_processor_web_server` - Python file that sets up our FLASK web server that processes images and requests
 + `processing.py` - Python file that the web server uses to process images. 
 + `requirements.txt` - Python packages that need to be installed in the virtual environment to run the project

 
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
To Use the GUI:

Upload:

  *	To upload images make sure images are all jpg or jpeg. This includes files in zip folder.
  *	If you desire to upload one image, click Upload JPG. Then select the image you would like to upload.
  *	Then click Confirm JPG Upload and wait approx. 15 seconds for server to process
  *	If you want to upload multiple images simply keep presses the Upload JPG button and selecting new files. Once you have selected all the files that you want click Confirm Upload and all images will be uploaded.
  *	For a zip file simply click Upload ZIP and select the file. It will automatically be uploaded upon selection.

Library:

  *	This window displays all the images within the database. Please give server ample time to load all photos
  *	To download photos click the add to list icon contained within the tile bar of image.
  *	Once you have clicked/selected all images you would like to download select your file type.
  *	Choose JPG, PNG, or TIFF, once clicked download will automatically begin, please give time for download to occur.
  *	Files will be downloaded within a zip file.

Enhance:

  *	This window is meant to enable user to enhance desired images.
  *	To enhance an image, click the camera icon on the respective image tile bar
  *	This will bring up the Enhance Editor page
  *	NOTE: Reverse Video enhancement should only work on greyscale images
  *	Page will display information about the image you have selected.
  *	To enhance an image, click one of the enhancement types on the top of page
  *	Wait for enhancement to complete, After Image will automatically change to processed image when finished.
  *	If you would like to save these changes press the Confirm Button.
  *	To enhance another image click the Upload or Library button and then click the Enhance button to allow you to select a new image to Enhance.


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


# Original Assignment Copied Below
BME590 Final Project

# Image Processor Final Project (Fall 2018)

**Final Project DUE:** Thursday, Dec 13, 2018 05:00PM EST 

## Overview
The final project in this class will require your team to leverage the
industry-standard skills you've learned over this semester to design and
implement a software system to upload an image or an archive of images to a
web-server, perform image-processing tasks on the web-server, and then display
/ download your processed image(s).  You will be required to work in your
groups for this projects.

This final project is somewhat open-ended to allow groups to tailor this to
their areas of interest; however, recommended datasets and project requirements
are provided below.  If you plan to stray away from the recommended projects
and datasets, please submit a one-page project proposal to Dr. Palmeri and Mr.
Kumar by *Friday, April, 13, 2018* for evaluation to ensure the proposed
project meets the requirements for the class. Be sure to include motivations,
technologies, functional specifications, and anticipated deliverables.

It is expected that your team will follow proper professional software
development and design conventions taught in this class, including:
* git feature-branch workflow
* continuous integration
* unit testing
* PEP8
* docstrings / Sphinx documentation

## Functional Specifications
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

## Deliverables
* A detailed `README` describing the final performance and state of your
  project.
* Recorded video demo of your image processor in action.
* All project code (in the form of a tagged GitHub repository named
  `bme590final`)
* Link to deployed web service 

## Recommended Datasets
Your project can utilize some existing databases of image (or you can choose to
use your own images).  Here are some example datasets that you can access for
this project:

* Over 13000 annotated skin lesion images are available from the International
  Skin Imaging Collaboration (ISIC) project that can be used to develop machine
  learning models to classify new images. This dataset can be accessed here:
  https://isic-archive.com. A zip of all annotated images can be downloaded by
  navigating to the Gallery and then clicking "Download as Zip" in the upper
  right hand corner. All data can also be accessed through a RESTful API
  provided by the ISIC.
* http://www.vision.caltech.edu/Image_Datasets/Caltech101/
* https://www.cs.toronto.edu/~kriz/cifar.html
* https://github.com/beamandrew/medical-data

## Grading
**You should approach this final project as an opportunity to show a potential
future employer an example of your software development skills.**

* Git Repository
  + Issues/Milestones
  + Commits are discrete, logical changesets
  + Feature-branch workflow
* Software best practices
  + Modularity of software code
  + Handling and raising exceptions
  + Language convention and style (PEP8)
  + Sphinx documentation for all modules/functions
* Testing and CI
  + Unit test coverage of all functions (except Flask handler)
  + Travis CI passing build
* Cloud-based Web Service
  + RESTful API Design 
  + Validation Logic 
  + Returning proper error codes
  + Robust deployment on virtual machine 
  + Image processing functionality
* Proper use of a database 
* User interface functionality
* Demo of the final working project
* Robust README
