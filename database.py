import os
import json
import datetime
from pymodm import connect
from pymodm import MongoModel, fields

from processing import Processing


class Image(MongoModel):
    image_id = fields.CharField(primary_key=True)
    filename = fields.CharField()
    image_data = fields.CharField()
    email = fields.CharField()
    timestamp = fields.DateTimeField()
    width = fields.IntegerField()
    height = fields.IntegerField()
    format = fields.CharField()
    description = fields.CharField()
    parent_id = fields.CharField()
    child_ids = fields.ListField()  # can have multiple children.
    process_history = fields.ListField()  # log of all previous IDs
    processing_time = fields.IntegerField()  # in milliseconds
    process = fields.CharField()  # the actual process that was done.


class User(MongoModel):
    email = fields.CharField(primary_key=True)
    # the structure of this will be key (upload id): most recent_id
    uploads = fields.DictField()
    current_image = fields.CharField()
    process_count = fields.DictField()


class ImageProcessingDB(object):
    def __init__(self, **kwargs):
        with open("config.json", 'r') as f:
            config_info = json.load(f)
            db_user = config_info["mongo_user"]
            db_pass = config_info["mongo_pass"]

            url = "mongodb://{}:{}@ds133378.mlab.com:33378/" \
                  "image_processing".format(db_user, db_pass)
            connect(url)

    def add_image(self, email, image_info):
        """
        Adds image to the database. First checks if it is a child of
        another image, then adds the image.
        Args:
            email: User who is adding the image.
            image_info: Information about the image.
        Returns:
            object: Image database object that was added.
        """
        current_time = datetime.datetime.now()
        image_info = self._image_parameter_check(image_info)
        # see if there is a parent-child relationship for the image.
        if "parent_id" in image_info.keys():
            # look for the provided id in the database
            parent_image = self.get_current_image(email)
            image_info["process_history"] = parent_image.process_history
            image_info["process_history"].append(image_info["image_id"])
            # relate the child to the parent
            self._add_child(image_info["image_id"],
                            image_info["parent_id"],
                            email)
        else:
            image_info["process_history"] = [image_info["image_id"]]
            image_info["parent_id"] = "root"

        # update user object as well.
        self.update_process_history(email, image_info["process_history"])
        self.update_user_current(email, image_info["image_id"])

        # deal with description
        if "description" not in image_info.keys():
            description = "None"
        else:
            description = image_info["description"]

        # add image to db
        i = Image(email=email,
                  filename=image_info["filename"],
                  image_id=image_info["image_id"],
                  process=image_info["process"],
                  image_data=image_info["image_data"],
                  processing_time=image_info["processing_time"],
                  process_history=image_info["process_history"],
                  parent_id=image_info["parent_id"],
                  width=image_info["width"],
                  height=image_info["height"],
                  format=image_info["format"],
                  timestamp=current_time,
                  description=description
                  )
        db_image = i.save()
        return db_image

    def get_current_image_id(self, email):
        """
        Obtains the user's current image id.
        Args:

        Returns:
            object:

        """
        user = self.find_user(email)
        if user is None:
            return None
        return user.current_image

    def get_current_image(self, email):
        """
        Obtains the user's current image.
        Args:
            email: user to get current image of.

        Returns:
            dict: user's current image.

        """
        image_id = self.get_current_image_id(email)
        image = self.find_image(image_id, email)
        return image

    def get_all_updated_images(self, email):
        """
        Gets all updated/recent images of a user.
        Args:
            email: User to get.

        Returns:
            list: All images as stored in database.

        """
        user = self.find_user(email)
        updated_list = []
        for root in user.uploads.keys():
            image_id = user.uploads[root]
            image = self.find_image(image_id, email)
            updated_list.append(image)

        return updated_list

    def get_all_original_images(self, email):
        """
        Gets all original images of a user.
        Args:
            email: User to get.

        Returns:
            list: All original images as stored in database.

        """
        user = self.find_user(email)
        original_list = []
        for image_id in user.uploads.keys():
            image = self.find_image(image_id, email)
            original_list.append(image)

        return original_list

    def _add_child(self, child_id, parent_id, email):
        """
        Adds a child id to the parent image.
        Args:
            parent_id: id of the parent to add the child id to.
            child_id: child id to add.

        Returns:
            str: child id of the image that was added.
        """
        parent_image = self.find_image(parent_id, email)
        if parent_image is not None:
            parent_image.child_ids.append(child_id)
            parent_image.save()
            return child_id
        return None

    def _image_parameter_check(self, image_info):
        """
        Tests if image input is valid.
        Args:
            image_info: Image object with imformation regarding
            image and history.

        Returns:
            bool: Whether or not the image_info object is valid.

        """
        if not isinstance(image_info, dict):
            raise TypeError("image_info must be type dict.")
        if "image_id" not in image_info.keys():
            raise AttributeError("image_info must have image_id.")
        if not isinstance(image_info["image_id"], str):
            raise ValueError("image_id must be type str.")
        if "email" not in image_info.keys():
            raise AttributeError("image_info must have email.")
        if not isinstance(image_info["email"], str):
            raise ValueError("email must be type str.")
        if "filename" not in image_info.keys():
            raise AttributeError("image_info must have filename.")
        if not isinstance(image_info["filename"], str):
            raise ValueError("filename must be type str.")
        if "image_data" not in image_info.keys():
            raise AttributeError("image_info must have image_data.")
        if type(image_info["image_data"]) != str:
            raise TypeError("image_data must be type str.")
        if "width" not in image_info.keys():
            raise AttributeError("image_info must have width.")
        if type(image_info["width"]) != int:
            raise TypeError("format must be type int")
        if "height" not in image_info.keys():
            raise AttributeError("image_info must have height.")
        if type(image_info["width"]) != int:
            raise TypeError("format must be type int")
        if type(image_info["format"]) != str:
            raise TypeError("format must be type str")
        if image_info["format"].lower() not in ["jpg", "jpeg", "png",
                                                "tiff", "gif", "none"]:
            raise ValueError("format invalid.")
        if "processing_time" not in image_info.keys():
            raise AttributeError("image_info must have processing_time.")
        if not isinstance(image_info["processing_time"], int):
            raise TypeError(
                "processing_time must be type int in milliseconds.")
        if "process" not in image_info.keys():
            raise AttributeError("image_info must have process.")
        if not isinstance(image_info["process"], str):
            raise TypeError("process must be type str.")
        if not self._valid_process(image_info["process"]):
            raise ValueError("process invalid.")
        return image_info

    def _valid_process(self, process):
        """
        Determines if the process is valid based on Processing methods.
        Args:
            process (str): process to check.

        Returns:
            bool: Whether or not the process is valid.

        """
        valid_processes = [func for func in dir(Processing)
                           if callable(getattr(Processing, func))]
        valid_processes.append('upload')
        if process not in valid_processes:
            return False
        return True

    def add_user(self, email):
        """
        Adds user to the database.
        Args:
            email: Unique identifier. Doesn't have to be ID.

        Returns:
            object: user object that was saved.

        """
        test_user = self.find_user(email)
        if test_user:
            raise ValueError("User already exists!")

        u = User(email=email)
        return u.save()

    def update_process_history(self, email, process_history: list):
        """
        Updates user uploads for an image.
        Args:
            process_history: History of Image ids.
            email: User to update.

        Returns:
            object: updated user object.
        """

        root_id = process_history[0]
        recent_id = process_history[-1]
        user = self.find_user(email)
        if user is None:
            user = self.add_user(email)
        user.uploads[root_id] = recent_id
        return user.save()

    def update_user_current(self, email, image_id):
        """
        Updates user current_image.
        Args:
            email: User to update.
            image_id: Id to update with

        """
        # image is not yet in the database
        user = self.find_user(email)
        if user is None:
            user = self.add_user(email)
        user.current_image = image_id
        return user.save()

    def update_user_process(self, email: str, process: str):
        """
        Increments the count on the process performed.
        Args:
            email (str): User to update.
            process (str): Id to update with

        """
        # image is not yet in the database
        if not self._valid_process(process):
            raise ValueError("process invalid.")

        user = self.find_user(email)
        if process not in user.process_count.keys():
            user.process_count[process] = 0
        user.process_count[process] += 1
        return user.save()

    def remove_image(self, image_id):
        """
        Removes the image from the database.
        DANGER: will not remove parent-child relationship!
        Args:
            image_id: ID of the image to remove.
        """
        for image in Image.objects.all():
            if str(image.image_id) == image_id:
                removed_image = image
                image.delete()
                return removed_image
        return None

    def find_image(self, image_id, email):
        """
        Finds the image in the database based on image id.
        Args:
            email: user ID for the image.
            image_id: ID of the image to find.

        Returns:
            object: found image in the database.
        """
        for image in Image.objects.all():
            if str(image.image_id) == image_id \
                    and str(image.email) == email:
                return image
        return None

    def find_image_parent(self, image_id, email):
        """
        Finds the parent of the image in the database based on image id.
        Args:
            image_id: ID of the image to find.

        Returns:
            object: found image in the database.
        """
        image = self.find_image(image_id, email)
        if image.parent_id is not None:
            parent_id = image.parent_id
            parent_image = self.find_image(parent_id, email)
            return parent_image
        return None

    def find_image_child(self, image_id, email):
        """
        Finds the child of the image in the database based on image id.
        Args:
            image_id: ID of the image to find.

        Returns:
            object: found image in the database.
        """
        image = self.find_image(image_id, email)
        if image is not None:
            return image.child_ids
        return []

    def find_user(self, email):
        """
        Finds user in the database and returns if found.
        Args:
            email: ID of user to find.

        Returns:
            object: found user in the database.

        """
        for user in User.objects.all():
            if str(user.email) == email:
                return user
        return None

    def image_to_json(self, image):
        """
        Gets returnable json format of image.
        Args:
            image:
        """

        ret_json = {
            "filename": image.filename,
            "image_id": image.image_id,
            "email": image.email,
            "parent_id": image.parent_id,
            "processing_history": image.process_history,
            "description": image.description,
            "image_data": image.image_data,
            "processing_time": image.processing_time,
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "child_ids": image.child_ids,
            "process": image.process,
            "timestamp": image.timestamp
        }
        return ret_json

    def user_to_json(self, user):
        """
        Gets returnable json format of user.
        Args:
            user:
        """
        ret_json = {
            "email": user.email,
            "uploads": user.uploads,
            "current_image": user.current_image,
            "process_count": user.process_count
        }
        return ret_json
