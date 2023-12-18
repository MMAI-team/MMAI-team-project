import base64
import keras.utils as image
import tensorflow as tf
from PIL import Image
from keras.applications import resnet
from tensorflow import keras
from keras import backend as K


class PathModel:
    def __init__(self, path, name="Path Model"):
        self.model = keras.models.load_model(path, custom_objects={"K": K})

        self.name = name

    def predict(self, data):
        first_photo_path, second_photo_path = data

        # open photos using opencv
        first_photo = self.preprocess(first_photo_path)
        second_photo = self.preprocess(second_photo_path)

        # expand dims
        first_photo = tf.expand_dims(first_photo, axis=0)
        second_photo = tf.expand_dims(second_photo, axis=0)

        input_images = {"img_1": first_photo, "img_2": second_photo}

        prediction = float(self.model(input_images, training=False))

        if prediction < 0.5:
            return "The images are not similar!"
        else:
            return "The images are similar!"

    def preprocess(self, img, scale=(224, 224)):
        img = Image.open(img)
        img = img.resize(scale)
        img_array = image.img_to_array(img)
        preprocessed_img = resnet.preprocess_input(img_array)
        return preprocessed_img


class APIModel:
    def __init__(self, sender, model_id, name="API Model"):
        self.sender = sender
        self.name = name
        self.model_id = model_id

    def predict(self, data):
        images = [open(photo, "rb") for photo in data]
        # encode using base64
        images = [base64.b64encode(image.read()).decode("utf-8") for image in images]

        # send the images to the API
        result = self.sender.predict(images, self.model_id)
        print(f"Result: {result}")
        if result:
            return "The images are similar!"
        else:
            return "The images are not similar!"
