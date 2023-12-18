import base64
import os
import uuid

import dotenv
from flask import Flask, jsonify, request
from models import PathModel

dotenv.load_dotenv()

app = Flask(__name__)

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH")
model = PathModel(MODEL_PATH, "CNN model")

app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Generate a unique identifier for this set of images
    unique_id = str(uuid.uuid4())

    # Decode and save the first image
    image_data1 = base64.b64decode(data["image1"])
    image_path1 = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}-1.jpg")
    with open(image_path1, "wb") as file:
        file.write(image_data1)

    # Decode and save the second image
    image_data2 = base64.b64decode(data["image2"])
    image_path2 = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}-2.jpg")
    with open(image_path2, "wb") as file:
        file.write(image_data2)

    # Process images with the model
    result = model.predict([image_path1, image_path2])

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
