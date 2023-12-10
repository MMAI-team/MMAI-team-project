from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import numpy as np
from models import PathModel

app = Flask(__name__)

# Model configuration
MODEL_PATH = "C:/Users/LiubomyrMaievskyi/Desktop/CNN.h5"
model = PathModel(MODEL_PATH, "CNN model")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Decode the first image
    image_data1 = base64.b64decode(data["image1"])
    image1 = Image.open(io.BytesIO(image_data1))

    # Decode the second image
    image_data2 = base64.b64decode(data["image2"])
    image2 = Image.open(io.BytesIO(image_data2))

    # Convert images to a format your model expects (e.g., numpy array)
    # This conversion depends on your model's requirement
    image_array1 = np.array(image1)
    image_array2 = np.array(image2)

    # Process images with the model
    result = model.predict([image_array1, image_array2])

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
