from flask import Flask, request, jsonify
import base64
import os
import uuid
from models import PathModel
from sift_matcher import SiftMatcher
from g_drive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload
import io
from tensorflow.keras import backend as K

app = Flask(__name__)


def download_model(file_id, local_file_path):
    if not os.path.exists(local_file_path):
        # Ensure the directory for the model exists
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        g_drive_service = GoogleDriveService().build()
        request = g_drive_service.files().get_media(fileId=file_id)

        with open(local_file_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print("Download Progress: {0}".format(status.progress() * 100))
        print(f"Model downloaded to {local_file_path}")
    else:
        print(f"Model already exists at {local_file_path}")


# Set the path for the CNN model file
MODEL_PATH_CNN = "./models/cnn_model.h5"

# Download the CNN model from Google Drive if it's not already downloaded
MODEL_FILE_ID = "1sTQn2ee8yktHvIirCwGV9XhId9v3dPu1"
download_model(MODEL_FILE_ID, MODEL_PATH_CNN)

model_cnn = PathModel(MODEL_PATH_CNN, "CNN model")
sift_matcher = SiftMatcher()

models = {"cnn": model_cnn, "sift": sift_matcher}

app.config["UPLOAD_FOLDER"] = "./test_images"

# Ensure the upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    model_id = data.get("modelId", "cnn")

    unique_id = str(uuid.uuid4())
    image_path1 = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}-1.jpg")
    image_path2 = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}-2.jpg")

    try:
        # Save and process images
        image_data1 = base64.b64decode(data["image1"])
        with open(image_path1, "wb") as file:
            file.write(image_data1)

        image_data2 = base64.b64decode(data["image2"])
        with open(image_path2, "wb") as file:
            file.write(image_data2)

        selected_model = models.get(model_id)
        if selected_model:
            if model_id == "sift":
                result = selected_model.predict(image_path1, image_path2)
            else:
                result = selected_model.predict([image_path1, image_path2])
        else:
            raise ValueError("Invalid modelId")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Delete the image files after processing
        if os.path.exists(image_path1):
            os.remove(image_path1)
        if os.path.exists(image_path2):
            os.remove(image_path2)

    return jsonify(result)


@app.route("/models", methods=["GET"])
def list_models():
    available_model_ids = list(models.keys())
    return jsonify(available_model_ids)


if __name__ == "__main__":
    app.run(debug=True)
