import requests
import json


class APISender:
    def __init__(self, address, endpoint):
        self.address = address
        self.endpoint = endpoint

    # recive a list of images and return a list of predictions
    def predict(self, images):
        # Prepare the data to be sent
        data = {"image1": images[0], "image2": images[1]}

        # Send the request
        response = requests.post(
            url=f"{self.address}/{self.endpoint}", json=data
        )

        # Return the response
        return response.json()

    def get_models(self):
        # mock models
        return [
            {"id": 1, "name": "CNN model"},
            {"id": 2, "name": "SVM model"},
            {"id": 3, "name": "Random Forest model"},
        ]
