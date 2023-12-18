import requests


class APISender:
    def __init__(self, address):
        self.address = address

    # recive a list of images and return a list of predictions
    def predict(self, images, model_id="sift"):
        # Prepare the data to be sent
        data = {
            "modelId": model_id,
            "image1": images[0],
            "image2": images[1],
        }

        # Send the request
        response = requests.post(url=f"{self.address}/predict", json=data)

        # Return the response
        return response.json()

    def get_models(self):
        response = requests.get(url=f"{self.address}/models")
        return response.json()

