from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

# initialize the Flask application.
app = Flask(__name__)
CORS(app)
# sets the directory where uplodaded files will be stored
UPLOAD_FOLDER = "uploads"
# defines the set of allowed file extensions for upload
ALLOWED_EXTENSIONS = {"pdf"}

# adds the upload folder to the applicaton's configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# checks if the filename has an allowed extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    # if there is no file part in the request, it returns a 400 error.
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}, 400)
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}, 400)
    if file:
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"message": f"File {filename} uploaded successfully"}, 200)
    else:
        return jsonify({"message": "File type not allowed"}, 400)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    # combines the upload folder and filename to get the full file path
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False, mimetype="application/pdf")
    else:
        return jsonify({"message": "File not found"}, 404)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
