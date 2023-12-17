from flask import Flask, request, jsonify
import base64
import os
import uuid
from models import PathModel
from sift_matcher import SiftMatcher

app = Flask(__name__)

# Model configuration
MODEL_PATH_CNN = "C:/Users/LiubomyrMaievskyi/Desktop/CNN.h5"
model_cnn = PathModel(MODEL_PATH_CNN, "CNN model")
sift_matcher = SiftMatcher()

# Dictionary to manage the models
models = {"cnn": model_cnn, "sift": sift_matcher}

app.config["UPLOAD_FOLDER"] = "C:/Users/LiubomyrMaievskyi/Desktop/test_images"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    model_id = data.get("modelId", "cnn")  # Default to 'cnn' if no modelId is provided

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

    selected_model = models.get(model_id)
    if selected_model:
        # Check if the model is SiftMatcher and call predict method accordingly
        if model_id == "sift":
            result = selected_model.predict(image_path1, image_path2)
        else:
            result = selected_model.predict([image_path1, image_path2])

        return jsonify(result)
    else:
        return jsonify({"error": "Invalid modelId"}), 400


@app.route("/models", methods=["GET"])
def list_models():
    available_model_ids = list(models.keys())
    return jsonify(available_model_ids)


if __name__ == "__main__":
    app.run(debug=True)
