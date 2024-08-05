import cv2
from pyzbar.pyzbar import decode
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    decoded_objects = decode(image)
    if not decoded_objects:
        return "No QR code found"
    for obj in decoded_objects:
        qr_data = obj.data.decode("utf-8")
        return qr_data
    return "Unable to read the QR code"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decode_qr', methods=['POST'])
def decode_qr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    text = read_qr_code(file_path)
    return jsonify({'decoded_text': text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

