from flask import Flask, request, jsonify
from models import PathModel
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
MODEL_PATH = "path/to/model"
model = PathModel(MODEL_PATH, "CNN model")
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if the post request has the file part
    if "file1" not in request.files or "file2" not in request.files:
        return "No file part"
    file1 = request.files["file1"]
    file2 = request.files["file2"]

    # If user does not select file, browser submits an empty part without filename
    if file1.filename == "" or file2.filename == "":
        return "No selected file"
    if (
        file1
        and file2
        and allowed_file(file1.filename)
        and allowed_file(file2.filename)
    ):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        file_path1 = os.path.join(app.config["UPLOAD_FOLDER"], filename1)
        file_path2 = os.path.join(app.config["UPLOAD_FOLDER"], filename2)
        file1.save(file_path1)
        file2.save(file_path2)

        # Process images with model
        result = model.predict([file_path1, file_path2])

        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
