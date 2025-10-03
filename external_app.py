import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
import requests

UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# API key yang dipakai service kompresor
COMPRESSOR_API_KEY = "secret123"

# URL service kompresor
COMPRESS_SERVICE_URL = "https://pdf.viscusmedia.com/compress"
CALLBACK_URL = "http://127.0.0.1:5000/receive"  # callback ke flask ini sendiri

app = Flask(__name__)
app.secret_key = "secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file:
            job_id = str(uuid.uuid4())
            filename = f"{job_id}.pdf"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Buat file_url lokal → supaya bisa diakses service kompresor
            # Dalam real case: file ini harus diupload ke storage publik (S3, dsb)
            file_url = f"http://127.0.0.1:5000/uploads/{filename}"

            # Panggil service kompresor
            payload = {
                "file_url": file_url,
                "dpi": 100,
                "callback_url": CALLBACK_URL,
            }

            resp = requests.post(COMPRESS_SERVICE_URL, json=payload)
            if resp.status_code == 200:
                flash(f"Job submitted! Job ID: {resp.json().get('job_id')}")
            else:
                flash(f"Failed to submit job: {resp.text}")

            return redirect(url_for("index"))

    # Tampilkan daftar file compressed yang sudah diterima
    files = os.listdir(COMPRESSED_FOLDER)
    return render_template("index.html", files=files)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    # Serve file uploaded supaya bisa diakses service kompresor
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/compressed/<filename>")
def compressed_file(filename):
    # Serve file compressed yang diterima dari callback
    return send_from_directory(COMPRESSED_FOLDER, filename)


@app.route("/receive", methods=["POST"])
def receive():
    api_key = request.headers.get("X-API-Key")
    if api_key != COMPRESSOR_API_KEY:
        return {"error": "Unauthorized"}, 401

    job_id = request.form.get("job_id")
    f = request.files.get("file")
    if not f:
        return {"error": "no file"}, 400

    filename = f"compressed_{job_id}.pdf"
    filepath = os.path.join(COMPRESSED_FOLDER, filename)
    f.save(filepath)

    print(f"📥 Received compressed file: {filepath}")
    return {"status": "ok", "job_id": job_id}, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
