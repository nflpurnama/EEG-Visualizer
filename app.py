import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, Response
from forms import upload_edf_form
from utils import convert_edf_to_b64
import io
import os
import tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

@app.route('/', methods=["GET", "POST"])
def viewer():
    return render_template('page/index.html') 

@app.route('/view', methods=['POST'])
def view_edf():
    # timestamp = request.form['timestamp']
    edf_file = request.files["file"]
    edf_bytes = edf_file.read()
    img_b64 = convert_edf_to_b64(edf_bytes=edf_bytes)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    timestamp = request.form['timestamp']
    edf_file = request.files["edf_file"]
    edf_bytes = edf_file.read()
    img_b64 = convert_edf_to_b64(edf_bytes=edf_bytes, start=timestamp)

    return jsonify({'result': "success"})


if __name__ == "__main__":
    app.run(debug=True)